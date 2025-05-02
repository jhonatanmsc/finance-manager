from rest_framework import routers

from goals.views import GoalViewSet

router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)
