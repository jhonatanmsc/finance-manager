from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers


class HistoryItemSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created_at = serializers.DateTimeField(default=now, required=False)
    updated_at = serializers.DateTimeField(default=now, required=False, allow_null=True)
