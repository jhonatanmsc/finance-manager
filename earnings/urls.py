from rest_framework import routers

from earnings.views import EarningViewSet

router = routers.DefaultRouter()
router.register(r"earnings", EarningViewSet)
