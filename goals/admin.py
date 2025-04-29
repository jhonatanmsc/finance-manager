from django.contrib import admin

from goals.admin_forms import SupplierForm
from goals.models import Goal, Contribution, Supplier
from src.custom_admin import CustomModelAdmin
from src.utils import real_currency
from django.utils.translation import gettext_lazy as admin_text


class GoalListFilter(admin.SimpleListFilter):
    title = admin_text("Objetivo")
    parameter_name = "goal"

    def lookups(self, request, model_admin):
        goals = Goal.objects.all()
        return [
            (goal.id, goal.title) for goal in goals
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(goal=self.value())


class SupplierListFilter(admin.SimpleListFilter):
    title = admin_text("Fornecedor")
    parameter_name = "supplier"

    def lookups(self, request, model_admin):
        suppliers = Supplier.objects.all()
        return [
            ("Nenhum", "Nenhum"),
            *[(supplier.id, supplier.name) for supplier in suppliers]
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "Nenhum":
                return queryset.filter(supplier=None)
            return queryset.filter(supplier=self.value())


@admin.register(Goal)
class GoalAdmin(CustomModelAdmin):
    list_display = ("title", "progress", "total", "budget")
    readonly_fields = ("total_descr", )

    def total(self, obj):
        return f"R$ {real_currency(obj.total)}"

    def budget(self, obj):
        return f"R$ {real_currency(obj.value)}"

    def progress(self, obj):
        return "%d%%" % ((obj.total / obj.value) * 100)


@admin.register(Contribution)
class ContributionAdmin(CustomModelAdmin):
    list_display = ("title", "description","value", "supplier", "goal", "group_name", "quantity", "total", "concluded_at", )
    # readonly_fields = ('users', )
    list_filter = [SupplierListFilter, GoalListFilter]

    def total(self, obj):
        return real_currency(obj.quantity * obj.value)


@admin.register(Supplier)
class SupplierAdmin(CustomModelAdmin):
    form = SupplierForm
    list_display = ("id", "name", "total", )
    # readonly_fields = ('users', )

    def total(self, obj):
        return "R$ " + real_currency(obj.total)
