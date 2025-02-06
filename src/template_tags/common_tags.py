import locale
from datetime import datetime

from django import template

register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)


@register.filter('real_currency')
def real_currency(value):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    value = locale.currency(value, grouping=True, symbol=False)
    return value


@register.filter('format_date')
def format_date(value: datetime):
    return value.strftime('%m/%Y')