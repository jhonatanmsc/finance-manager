from src.model_admin import CustomModelAdmin


class CreditAdmin(CustomModelAdmin):
    exclude = ('users',)