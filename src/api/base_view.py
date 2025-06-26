from datetime import datetime

from django.db import models
from requests import Response
from rest_framework import permissions, serializers, viewsets

from src.api.serializers import HistoryItemSerializer
from src.utils import br_tz


class BaseViewSet(viewsets.ModelViewSet):
    queryset: models.QuerySet = None
    serializer_class: serializers.SerializerMetaclass = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(deactivated_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        instance: models.Model = self.get_object()
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
        return Response(self.serializer_class(instance).data, status=200)
