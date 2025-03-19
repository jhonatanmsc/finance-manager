from django.contrib import admin

from goals.admin_forms import SupplierForm
from goals.models import Goal, Contribution, Supplier
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
class GoalAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ("title", "total",)
    readonly_fields = ("total_descr",)

    def total(self, obj):
        return f"R$ {real_currency(obj.total)} / R$ {real_currency(obj.value)}"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ("title", "description","value", "supplier", "goal", "group_name", "quantity", "total", "concluded_at")
    list_filter = [SupplierListFilter, GoalListFilter]

    def total(self, obj):
        return real_currency(obj.quantity * obj.value)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    form = SupplierForm
    list_display = ("id", "name", "total")

    def total(self, obj):
        return "R$ " + real_currency(obj.total)
