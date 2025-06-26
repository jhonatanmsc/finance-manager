from goals.models import Goal
from goals.serializers import GoalSerializer
from src.api.base_view import BaseViewSet


class GoalViewSet(BaseViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
