from django.db import models
from django.utils.translation import gettext_lazy as admin_text


class RecurrenceEnum(models.TextChoices):
    YEAR = 'YEAR', admin_text('Anual')
    MONTH = 'MONTHLY', admin_text('Mensal')
    WEEK = 'WEEK', admin_text('Semanal')
    NONE = 'N', admin_text('Sem')


class InvestmentTypeEnum(models.TextChoices):
    POST_FIXED = 'POST_FIXED', admin_text('Pós-Fixado')
    PRE_FIXED = 'PRE_FIXED', admin_text('Pré-Fixado')
    HYBRID = 'HYBRID', admin_text('Híbrido')
    VARIABLE = 'VARIABLE', admin_text('Renda Variável')
    STOCK = 'STOCK', admin_text('Ações')
    FUND = 'FUND', admin_text('Fundo de Investimento')
    REAL_ESTATE = 'REAL_ESTATE', admin_text('Imóveis')
    CRYPTOCURRENCY = 'CRYPTOCURRENCY', admin_text('Criptomoedas')
    SAVINGS = 'SAVINGS', admin_text('CDI')


class CreditTypeEnum(models.TextChoices):
    CARD = 'CARD', admin_text('Cartão')
    LOAN = 'LOAN', admin_text('Empréstimo')
    MORTGATE = 'MORTGATE', admin_text('Hipoteca')
    CASH_ADVANCE = 'CASH_ADVANCE', admin_text('Adiantamento de Dinheiro')