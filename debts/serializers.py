from rest_framework import serializers

from debts.models import Debt


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = [
            "id",
            "title",
            "description",
            "value",
            "recurrence",
            "created_at",
            "updated_at",
            "history",
            "due_day",
            "users",
            "due_date",
            "credit_card",
            "payment_method",
        ]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if "value" in validated_data:
            validated_data["value"] = float(validated_data["value"])

        return validated_data
