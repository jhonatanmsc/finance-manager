import json

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.utils import real_currency


class Supplier(models.Model):
    __tablename__ = 'suppliers'
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    rating = models.IntegerField(default=0, choices=[(i, f'{i/2} estrelas') for i in range(1, 10)],
                                 verbose_name="Avaliação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"


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

    # @property
    # def total(self):
    #     contrib = {}
    #     total_value = 0
    #     for con in self.contributions.all():
    #         if contrib.get(con.group_name):
    #             contrib[con.group_name] += con.total
    #         else:
    #             contrib[con.group_name] = con.total
    #         total_value += con.total
    #     result = "\n".join([f"{k}: {real_currency(contrib[k])}" for k in contrib])
    #     result += f"\n\n*Total*: R$ {real_currency(total_value)}"
    #     return result

    def set_history(self, history):
        self.history = json.dumps(history)

    def get_history(self):
        return json.loads(self.history)

    def add_history(self, item):
        self.history.append(item)
        return self.history

    def __str__(self):
        return f"{self.title}"

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
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Fornecedor", related_name="contributions_new")
    group_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Grupo")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, verbose_name="Quantidade")

    @property
    def total(self):
        return self.quantity * self.value

    def __str__(self):
        return f"{self.title} | {self.concluded_at.strftime('%d/%m/%Y')} | {self.group_name} |{self.goal.title}"

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"
