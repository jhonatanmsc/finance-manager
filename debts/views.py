from debts.models import Debt
from debts.serializers import DebtSerializer
from src.api.base_view import BaseViewSet


class DebtViewSet(BaseViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
