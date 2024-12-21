# Generated by Django 5.1.4 on 2024-12-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.CharField(blank=True, help_text='Formato aceito DD-MM', max_length=5, null=True, verbose_name='Dia do recebimento')),
                ('category', models.CharField(choices=[('CARD', 'Cartão'), ('LOAN', 'Empréstimo'), ('MORTGATE', 'Hipoteca'), ('CASH_ADVANCE', 'Adiantamento de Dinheiro')], default='CARD', max_length=100, verbose_name='Categoria')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('history', models.CharField(max_length=200, verbose_name='Histórico')),
            ],
            options={
                'verbose_name': 'Crédito',
                'verbose_name_plural': 'Opções de Crédito',
            },
        ),
    ]
