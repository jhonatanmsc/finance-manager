from django.contrib import admin

from investments.models import Investment
from src.custom_admin import CustomModelAdmin


@admin.register(Investment)
class InvestmentAdmin(CustomModelAdmin):
    exclude = ('users',)
