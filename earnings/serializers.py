from rest_framework import serializers

from earnings.models import Earning


class EarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earning
        fields = [
            "id",
            "title",
            "description",
            "value",
            "recurrence",
            "created_at",
            "updated_at",
            "history",
            "payment_day",
            "users",
            "expiration_date",
            "payer_type",
        ]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if "value" in validated_data:
            validated_data["value"] = float(validated_data["value"])

        return validated_data
