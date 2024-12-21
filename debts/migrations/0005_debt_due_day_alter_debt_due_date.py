# Generated by Django 5.1.4 on 2024-12-21 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0004_alter_debt_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='due_day',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Vencimento'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de vencimento'),
        ),
    ]
