# Generated by Django 5.1.4 on 2024-12-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='history',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Histórico'),
        ),
    ]
