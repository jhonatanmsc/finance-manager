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
