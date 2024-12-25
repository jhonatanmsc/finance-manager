import json

from django.contrib.auth.models import User
from django.db import models


class Goal(models.Model):
    __tablename__ = 'goals'
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")
    history = models.CharField(max_length=200, null=True, blank=True, verbose_name="Histórico")
    target_date = models.DateField(null=True, blank=True, verbose_name="Estimativa de Conclusão")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="goals", null=True, blank=True)
    concluded_at = models.DateTimeField(null=True, blank=True, verbose_name="Concluído em")
    canceled_at = models.DateTimeField(null=True, blank=True, verbose_name="Cancelado em")

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
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"


class Contribution(models.Model):
    __tablename__ = 'contributions'
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="contributions", null=True, blank=True)
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="contributions", verbose_name="Objetivo"
    )
    concluded_at = models.DateTimeField(null=True, blank=True, verbose_name="Executado em")
    supplier = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fornecedor")
    group_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Grupo")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, verbose_name="Quantidade")

    def __str__(self):
        return f"{self.title} | {self.concluded_at.strftime('%m/%Y')} | {self.group_name} |{self.goal.title}"

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"
