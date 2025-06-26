from rest_framework import routers

from debts.views import DebtViewSet

router = routers.DefaultRouter()
router.register(r"debt", DebtViewSet)
