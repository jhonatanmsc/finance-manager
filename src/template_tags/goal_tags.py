from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter("get_amount")
def get_amount(contributions:QuerySet) -> float:
    total = 0
    for contrib in contributions.all():
        total += contrib.value
    return total