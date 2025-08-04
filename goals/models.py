from decimal import Decimal

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from src.base_model import BaseModel


class Supplier(BaseModel):
    __tablename__ = "suppliers"
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    rating = models.IntegerField(
        default=0,
        choices=[(i, f"{i} estrelas") for i in range(1, 5)],
        verbose_name="Avaliação",
    )
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)

    @property
    def total(self):
        total_value = cache.get(f"supplier:{self.id}:total_contributions", 0)
        return total_value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"


class Goal(BaseModel):
    __tablename__ = "goals"
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    target_date = models.DateField(null=True, blank=True, verbose_name="Estimativa de Conclusão")
    users = models.ManyToManyField(User, verbose_name="Usuários", blank=True)
    master = models.ForeignKey(
        "Goal",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Objetivo pai",
        related_name="sub_goals",
    )
    concluded_at = models.DateField(null=True, blank=True, verbose_name="Concluído em")
    canceled_at = models.DateField(null=True, blank=True, verbose_name="Cancelado em")
    deactivated_at = models.DateField(null=True, blank=True, verbose_name="Desativado em")

    @property
    def total(self):
        lc_total = cache.get(f"goal:{self.id}:children_total", 0)
        total_contributions = cache.get(f"goal:{self.id}:total_contributions", 0)
        return total_contributions + lc_total

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"


class Contribution(BaseModel):
    __tablename__ = "contributions"
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Desconto (%)")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, verbose_name="Quantidade")
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name="Objetivo",
    )
    concluded_at = models.DateField(default=timezone.now, null=True, blank=True, verbose_name="Executado em")
    supplier = models.ForeignKey(
        Supplier,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Fornecedor",
        related_name="contributions",
    )
    group_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Grupo")

    @property
    def total(self):
        calc_discount = Decimal((100 - self.discount) / 100)
        total = self.quantity * Decimal(self.value) * calc_discount
        return total

    def __str__(self):
        return f"{self.title} | {self.concluded_at.strftime('%d/%m/%Y')} | {self.group_name} |{self.goal.title}"

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"
