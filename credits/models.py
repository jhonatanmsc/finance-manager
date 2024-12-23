import json

from django.contrib.auth.models import User
from django.db import models

from src.enums import CreditTypeEnum


class Credit(models.Model):
    __tablename__ = 'credits'
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.CharField(max_length=5, null=True, blank=True, verbose_name="Dia do vencimento")
    category = models.CharField(max_length=100, choices=CreditTypeEnum.choices, default=CreditTypeEnum.CARD, verbose_name="Categoria")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="credits", null=True, blank=True)
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")

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
        verbose_name = "Crédito"
        verbose_name_plural = "Opções de Crédito"