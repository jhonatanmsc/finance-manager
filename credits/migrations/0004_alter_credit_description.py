# Generated by Django 5.1.4 on 2024-12-21 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0003_alter_credit_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição'),
        ),
    ]
