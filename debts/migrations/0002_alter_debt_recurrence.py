# Generated by Django 5.1.4 on 2024-12-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='recurrence',
            field=models.CharField(choices=[('YEAR', 'Anual'), ('MONTHLY', 'Mensal'), ('WEEK', 'Semanal'), ('N', 'Sem')], default='N', max_length=50, verbose_name='Recorrência'),
        ),
    ]