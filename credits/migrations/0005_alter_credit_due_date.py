# Generated by Django 5.1.4 on 2024-12-21 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0004_alter_credit_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='due_date',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Dia do vencimento'),
        ),
    ]
