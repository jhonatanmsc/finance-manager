from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from goals.models import Goal
from goals.serializers import GoalSerializer


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
