from src.model_admin import CustomModelAdmin


class ParameterAdmin(CustomModelAdmin):
    exclude = ('users',)
