from src.admin.model_admin import CustomModelAdmin


class ParameterAdmin(CustomModelAdmin):
    exclude = ("users",)
