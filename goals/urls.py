from rest_framework import routers

from goals.views import ContributionViewSet, GoalViewSet, SupplierViewSet

router = routers.DefaultRouter()
router.register(r"goals", GoalViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"contributions", ContributionViewSet)
