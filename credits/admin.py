from src.admin.model_admin import CustomModelAdmin


class CreditAdmin(CustomModelAdmin):
    exclude = ("users",)
