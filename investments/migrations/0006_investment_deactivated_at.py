# Generated by Django 5.1.4 on 2024-12-23 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0005_alter_investment_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='deactivated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Desativado em'),
        ),
    ]
