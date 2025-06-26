from earnings.models import Earning
from earnings.serializers import EarningSerializer
from src.api.base_view import BaseViewSet


class EarningViewSet(BaseViewSet):
    queryset = Earning.objects.all()
    serializer_class = EarningSerializer
