from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from credits.admin import CreditAdmin
from credits.models import Credit
from debts.admin import DebtAdmin
from debts.models import Debt
from earnings.admin import EarningsAdmin
from earnings.models import Earning
from goals.admin import ContributionAdmin, GoalAdmin, SupplierAdmin
from goals.models import Contribution, Goal, Supplier
from investments.admin import InvestmentAdmin
from investments.models import Investment
from parameters.admin import ParameterAdmin
from parameters.models import Parameter


class CustomAdminSite(admin.AdminSite):
    site_header = "Financeman💰"
    site_title = "Gerenciador Financeiro"

    def each_context(self, request):
        context = super().each_context(request)
        context["site_url"] = "/api/"
        return context


admin_site = CustomAdminSite(name="myadmin")
admin.site = admin_site
sites.site = admin_site

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Credit, CreditAdmin)
admin_site.register(Debt, DebtAdmin)
admin_site.register(Earning, EarningsAdmin)
admin_site.register(Goal, GoalAdmin)
admin_site.register(Contribution, ContributionAdmin)
admin_site.register(Supplier, SupplierAdmin)
admin_site.register(Investment, InvestmentAdmin)
admin_site.register(Parameter, ParameterAdmin)
