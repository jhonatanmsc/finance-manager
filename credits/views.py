from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from credits.models import Credit
from credits.serializers import CreditSerializer
from src.serializers import HistoryItemSerializer
from src.utils import br_tz


class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Credit.objects.filter(deactivated_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        instance: Credit = self.get_object()
        if "reason" not in request.data:
            return Response({"error": "Nenhuma razão foi informada"}, status=400)
        hist_item = HistoryItemSerializer(
            data={
                "title": "Crédito desativado",
                "description": request.data["reason"],
                "author": request.user.id,
            }
        )
        hist_item.is_valid(raise_exception=True)
        instance.history.append(hist_item.data)
        instance.deactivated_at = datetime.now(br_tz)
        instance.save()
        return Response(CreditSerializer(instance).data, status=200)
