# Generated by Django 5.1.4 on 2024-12-20 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings', '0003_alter_earnings_options_earnings_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='payment_day',
            field=models.CharField(blank=True, help_text='Formato aceito DD-MM', max_length=5, null=True, verbose_name='Dia do recebimento'),
        ),
    ]
