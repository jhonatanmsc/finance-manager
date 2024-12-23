# Generated by Django 5.1.4 on 2024-12-23 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('index', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('history', models.CharField(blank=True, max_length=200, null=True, verbose_name='Histórico')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='configs', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Parâmetro',
                'verbose_name_plural': 'Parâmetros',
            },
        ),
    ]