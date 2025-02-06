#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# from goals.models import Contribution


def map_all():
    m_map = {
        "Jaime": 1,
        "Dominó Teresina": 1,
        "Ramos": 1,
        "Depósito Piauí": 1,
        "Simão & CIA": 1,
        "Madeireira R.Fonsêca": 1,
        "JM Pré moldados": 1,
        "100tenário": 1,
        "Talysson Construções": 1,
        "Elinaldo & CIA": 1,
        "Ferro Norte": 1,
        "Elton": 1,
    }

    # objs = Contribution.objects.all()
    # for obj in objs:
    #     obj.supplier_new = m_map[obj.supplier]
    #     obj.save()
    # print("Done.")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
