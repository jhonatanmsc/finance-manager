from django.contrib.auth.models import User
from django.db import models


class Parameter(models.Model):
    __tablename__ = "parameters"
    name = models.CharField(max_length=100, verbose_name="Nome")
    index = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Índice")
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    history = models.JSONField(default=list, null=False, blank=True, verbose_name="Histórico")
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="Desativado em")

    def __str__(self):
        return f"#{self.id} {self.name}"

    class Meta:
        verbose_name = "Parâmetro"
        verbose_name_plural = "Parâmetros"
