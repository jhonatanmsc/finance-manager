from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from goals.models import Goal
from goals.serializers import GoalSerializer
from src.serializers import HistoryItemSerializer
from src.utils import br_tz


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(deactivated_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        instance: Goal = self.get_object()
        if "reason" not in request.data:
            return Response({"error": "Nenhuma razão foi informada"}, status=400)
        hist_item = HistoryItemSerializer(
            data={
                "title": "Objetivo desativado",
                "description": request.data["reason"],
                "author": request.user.id,
            }
        )
        hist_item.is_valid(raise_exception=True)
        instance.history.append(hist_item.data)
        instance.deactivated_at = datetime.now(br_tz)
        instance.save()
        return Response(GoalSerializer(instance).data, status=200)
