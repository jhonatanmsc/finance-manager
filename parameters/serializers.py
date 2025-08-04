from rest_framework import serializers

from parameters.models import Parameter


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = [
            "id",
            "name",
            "index",
            "description",
            "users",
            "created_at",
        ]
