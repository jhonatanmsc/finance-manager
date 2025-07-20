from src.admin.model_admin import CustomModelAdmin


class InvestmentAdmin(CustomModelAdmin):
    exclude = ("users",)
