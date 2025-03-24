import json

from django.contrib.auth.models import User
from django.db import models

from src.enums import CreditTypeEnum
from src.utils import real_currency


class Credit(models.Model):
    __tablename__ = 'credits'
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.CharField(max_length=5, null=True, blank=True, verbose_name="Dia do vencimento")
    category = models.CharField(max_length=100, choices=CreditTypeEnum.choices, default=CreditTypeEnum.CARD, verbose_name="Categoria")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        usado = sum([debt.value for debt in self.debts.all()])
        total = f"usando R$ {real_currency(usado)} de R$ {real_currency(self.limit)} disponível"
        return f"#{self.id} {self.title} | {total}"

    class Meta:
        verbose_name = "Crédito"
        verbose_name_plural = "Opções de Crédito"