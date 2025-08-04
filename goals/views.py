from rest_framework import viewsets

from goals.models import Contribution, Goal, Supplier
from goals.serializers import ContributionSerializer, GoalSerializer, SupplierSerializer
from src.api.base_view import BaseViewSet


class GoalViewSet(BaseViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.only(
            "title",
            "description",
            "value",
            "target_date",
            "master",
            "concluded_at",
            "canceled_at",
        )
        queryset = self.paginate_queryset(queryset)
        queryset = self.serializer_class(queryset, many=True).data
        return self.get_paginated_response(queryset)


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.only("name", "description", "rating")
        queryset = self.paginate_queryset(queryset)
        queryset = self.serializer_class(queryset, many=True).data
        return self.get_paginated_response(queryset)


class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        goal_ids = [int(id) for id in request.query_params.get("goals[]", [])]
        supplier_ids = [int(id) for id in request.query_params.get("suppliers[]", [])]
        if goal_ids:
            queryset = queryset.filter(goal__id__in=goal_ids)
        if supplier_ids:
            queryset = queryset.filter(supplier__id__in=supplier_ids)
        queryset = queryset.only(
            "id", "title", "description", "discount", "value", "quantity", "created_at", "goal", "supplier"
        )
        queryset = queryset.order_by("-created_at")
        queryset = self.paginate_queryset(queryset)
        queryset = self.serializer_class(queryset, many=True).data
        suppliers = {it.id: {"id": it.id, "name": it.name} for it in Supplier.objects.all()}
        goals = {it.id: {"id": it.id, "title": it.title} for it in Goal.objects.filter(deactivated_at__isnull=True)}
        for it in queryset:
            it["supplier"] = suppliers.get(it["supplier"], {"id": "", "name": " - - - "})
            it["goal"] = goals.get(it["goal"], {"id": "", "title": " - - - "})

        return self.get_paginated_response(queryset)
