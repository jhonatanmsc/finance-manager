from django.contrib import admin

from credits.models import Credit
from src.custom_admin import CustomModelAdmin


@admin.register(Credit)
class CreditAdmin(CustomModelAdmin):
    exclude = ('users',)