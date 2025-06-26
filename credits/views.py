from credits.models import Credit
from credits.serializers import CreditSerializer
from src.api.base_view import BaseViewSet


class CreditViewSet(BaseViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
