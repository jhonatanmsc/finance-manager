from rest_framework import serializers

from credits.models import Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = [
            "title",
            "description",
            "limit",
            "due_date",
            "category",
            "updated_at",
            "history",
            "users",
        ]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if "limit" in validated_data:
            validated_data["limit"] = float(validated_data["limit"])

        return validated_data
