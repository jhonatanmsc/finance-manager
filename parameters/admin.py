from django.contrib import admin

from parameters.models import Parameter
from src.custom_admin import CustomModelAdmin


@admin.register(Parameter)
class ParameterAdmin(CustomModelAdmin):
    exclude = ('users',)
