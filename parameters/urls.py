from rest_framework import routers

from parameters.views import ParameterViewSet

router = routers.DefaultRouter()
router.register(r"parameters", ParameterViewSet)
