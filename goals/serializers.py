from rest_framework import serializers

from goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id", "title", "description", "value", "created_at", "updated_at", "history",
            "target_date", "users", "master", "concluded_at", "canceled_at", "total"
        ]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if 'value' in validated_data:
            validated_data['value'] = float(validated_data['value'])

        return validated_data

    def get_total(self, obj):
        return round(obj.total, 2)