import json
from decimal import Decimal

from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

from src.utils import real_currency


class Supplier(models.Model):
    __tablename__ = 'suppliers'
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    rating = models.IntegerField(default=0, choices=[(i, f'{i/2} estrelas') for i in range(1, 10)],
                                 verbose_name="Avaliação")
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")

    @property
    def total(self):
        total_value = 0
        for con in self.contributions.all():
            total_value += con.total
        return total_value

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
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    master = models.ForeignKey("Goal", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Objetivo pai", related_name="sub_goals")
    concluded_at = models.DateField(null=True, blank=True, verbose_name="Concluído em")
    canceled_at = models.DateField(null=True, blank=True, verbose_name="Cancelado em")

    @property
    def total(self):
        lc_total = sum([go.total for go in self.sub_goals.all()])
        total_value = sum([con.total for con in self.contributions.all()])
        return total_value + lc_total

    @property
    def total_descr(self):
        contrib = {}
        total_value = 0
        for con in self.contributions.all():
            if contrib.get(con.group_name):
                contrib[con.group_name] += con.total
            else:
                contrib[con.group_name] = con.total
            total_value += con.total
        result = "\n".join([f"{k}: {real_currency(contrib[k])}" for k in contrib])
        result += f"\n\n*Total*: R$ {real_currency(total_value)}"
        return result

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
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Desconto (%)")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, verbose_name="Quantidade")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="contributions", verbose_name="Objetivo"
    )
    concluded_at = models.DateField(default=timezone.now, null=True, blank=True, verbose_name="Executado em")
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Fornecedor", related_name="contributions")
    group_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Grupo")


    @property
    def total(self):
        return self.quantity * self.value * Decimal((100 - self.discount) / 100)

    def __str__(self):
        return f"{self.title} | {self.concluded_at.strftime('%d/%m/%Y')} | {self.group_name} |{self.goal.title}"

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"
