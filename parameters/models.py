import json

from django.contrib.auth.models import User
from django.db import models


class Parameter(models.Model):
    __tablename__ = 'parameters'
    name = models.CharField(max_length=100, verbose_name="Nome")
    index = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Índice")
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="configs", null=True,
                             blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        return f"#{self.id} {self.name}"

    class Meta:
        verbose_name = "Parâmetro"
        verbose_name_plural = "Parâmetros"