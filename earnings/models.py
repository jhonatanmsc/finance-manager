import json

from django.contrib.auth.models import User
from django.db import models

from src.enums import RecurrenceEnum, PayerTypeEnum


class Earning(models.Model):
    __tablename__ = 'earnings'
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    recurrence = models.CharField(max_length=50, choices=RecurrenceEnum.choices, default=RecurrenceEnum.NONE, verbose_name="Recorrência")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    payment_day = models.CharField(max_length=5, null=True, blank=True, verbose_name="Dia do recebimento")
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name="Válido até")
    payer_type = models.CharField(max_length=50, choices=PayerTypeEnum.choices, default=PayerTypeEnum.PF, verbose_name="Tipo")

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        expiration = "Indeterminado" if self.expiration_date is None else self.expiration_date.strftime('%d/%m/%Y')
        return f"#{self.id} {self.title} | {expiration}"

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"