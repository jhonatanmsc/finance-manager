# Generated by Django 5.1.4 on 2025-01-08 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings', '0010_earning_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='earning',
            name='payer_type',
            field=models.CharField(choices=[('PF', 'Prato Feito'), ('PJ', 'Pratos do José')], default='PF', max_length=50, verbose_name='Tipo'),
        ),
    ]
