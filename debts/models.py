import json

from django.contrib.auth.models import User
from django.db import models

from credits.models import Credit
from src.enums import RecurrenceEnum, PaymentMethod
from src.utils import real_currency


class Debt(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    recurrence = models.CharField(max_length=50, choices=RecurrenceEnum.choices, default=RecurrenceEnum.NONE,
                                  verbose_name="Recorrência")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    due_day = models.CharField(max_length=5, null=True, blank=True, verbose_name="Vencimento")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="debts", null=True, blank=True)
    due_date = models.DateField(null=True, blank=True, verbose_name="Data de vencimento")
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")
    credit_card = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Cartão de credito", related_name="debts", null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CASH, verbose_name="Método de pagamento")

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        origem = "CC" if not self.credit_card else self.credit_card.title
        return f"#{self.id} {self.title} | {self.payment_method} | R$ {real_currency(self.value)} {origem}"

    class Meta:
        verbose_name = "Débito"
        verbose_name_plural = "Débitos"
