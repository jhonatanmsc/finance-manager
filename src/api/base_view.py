from datetime import datetime

from django.contrib.admin.models import DELETION
from django.db import models
from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response

from src.base_model import BaseModel
from src.utils import br_tz


class BaseViewSet(viewsets.ModelViewSet):
    queryset: models.QuerySet = None
    serializer_class: serializers.SerializerMetaclass = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(deactivated_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        instance: BaseModel = self.get_object()
        if "reason" not in request.data:
            return Response({"error": "Nenhuma razão foi informada"}, status=400)

        instance.add_log_entry(
            user_id=request.user.pk,
            reason=request.data["reason"],
            flag=DELETION,
        )

        instance.deactivated_at = datetime.now(br_tz)
        instance.save()
        return Response(self.serializer_class(instance).data, status=204)
