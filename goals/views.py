from goals.models import Contribution, Goal, Supplier
from goals.serializers import ContributionSerializer, GoalSerializer, SupplierSerializer
from src.api.base_view import BaseViewSet


class GoalViewSet(BaseViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ContributionViewSet(BaseViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(self.queryset)
        queryset = self.serializer_class(queryset, many=True).data
        suppliers = {it.id: {"id": it.id, "name": it.name} for it in Supplier.objects.all()}
        goals = {it.id: {"id": it.id, "title": it.title} for it in Goal.objects.filter(deactivated_at__isnull=True)}
        for it in queryset:
            it["supplier"] = suppliers.get(it["supplier"], {"id": "", "name": " - - - "})
            it["goal"] = goals.get(it["goal"], {"id": "", "title": " - - - "})

        return self.get_paginated_response(queryset)
