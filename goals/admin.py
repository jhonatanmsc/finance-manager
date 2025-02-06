from django.contrib import admin

from goals.admin_forms import SupplierForm
from goals.models import Goal, Contribution, Supplier
from src.utils import real_currency
from django.utils.translation import gettext_lazy as admin_text


class SupplierListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = admin_text("Fornecedor")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "supplier"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        suppliers = Supplier.objects.all()
        return [
            ("Nenhum", "Nenhum"),
            *[(supplier.id, supplier.name) for supplier in suppliers]
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            if self.value() == "Nenhum":
                return queryset.filter(supplier=None)
            return queryset.filter(supplier=self.value())


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    exclude = ('user',)
    # readonly_fields = ("total",)

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
    list_display = ("title", "value", "supplier", "goal", "group_name", "quantity", "total", "concluded_at")
    list_filter = [SupplierListFilter]

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
    list_display = ("id", "name",)
