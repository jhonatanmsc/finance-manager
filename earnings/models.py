import json

from django.contrib.auth.models import User
from django.db import models

from src.enums import RecurrenceEnum


# Create your models here.

class Earnings(models.Model):
    __tablename__ = 'earnings'
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    recurrence = models.CharField(max_length=50, choices=RecurrenceEnum.choices, default=RecurrenceEnum.NONE, verbose_name="Recorrência")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    payment_day = models.CharField(max_length=5, null=True, blank=True, verbose_name="Dia do recebimento")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="earnings", null=True, blank=True)

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        return f"#{self.id} {self.title}"

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"