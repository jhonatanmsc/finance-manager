from parameters.models import Parameter
from parameters.serializers import ParameterSerializer
from src.api.base_view import BaseViewSet


class ParameterViewSet(BaseViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
