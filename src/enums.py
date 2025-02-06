from django.db import models
from django.utils.translation import gettext_lazy as admin_text


class PaymentMethod(models.TextChoices):
    CASH = "CASH", admin_text("Dinheiro")
    CREDIT_CARD = "CREDIT_CARD", admin_text("Cartão de crédito")
    DEBIT_CARD = "DEBIT_CARD", admin_text("Cartão de débito")
    BANK_TRANSFER = "BANK_TRANSFER", admin_text("Transferencia bancária")
    DIGITAL_WALLET = "DIGITAL_WALLET", admin_text("Digitall wallet")
    CRYPTOCURRENCY = "CRYPTOCURRENCY", admin_text("Cryptocurrency")
    CHECK = "CHECK", admin_text("Check")
    OTHER = "OTHER", admin_text("Other")


class PayerTypeEnum(models.TextChoices):
    PF = "PF", admin_text("Prato Feito")
    PJ = "PJ", admin_text("Pratos do José")


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