from datetime import datetime

from django import urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView

from debts.models import Debt
from earnings.models import Earning
from goals.models import Goal
from parameters.models import Parameter
from src import settings
from src.enums import RecurrenceEnum
from src.utils import real_currency, get_last_9_months, get_ipca


class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect(urls.reverse('admin:login'))
        current_month = datetime.now().month
        current_year = datetime.now().year
        last_9_months = get_last_9_months()
        past_months = get_last_9_months('number')
        recurrence_debts = (
            Debt.objects
            .filter(user=self.request.user)
            .exclude(
                recurrence=RecurrenceEnum.NONE,
                due_date=None
            )
        )
        extra_debts = (
            Debt.objects
            .filter(user=self.request.user, created_at__month=current_month, created_at__year=current_year)
        )
        last_debts = (
            Debt.objects
            .filter(user=self.request.user, created_at__month__in=past_months, created_at__year=current_year)
            .order_by('-created_at')
        )
        last_debts_total = []
        for m in past_months:
            total_month = 0
            for deb in last_debts:
                if m == deb.created_at.month:
                    total_month += deb.value
            last_debts_total.append(float(total_month))

        debts = recurrence_debts.union(extra_debts)
        debts = sum([debt.value for debt in debts])
        emergency_fund = Parameter.objects.filter(user=self.request.user, name='reserva_1').first()
        emergency_fund = emergency_fund.index
        goal = Goal.objects.filter(user=self.request.user, title="Reserva de Médio prazo").first()
        context['debts'] = real_currency(debts)
        context['emergency_fund'] = real_currency(debts * emergency_fund)
        context['mid_fund'] = real_currency(goal.value)
        context['long_fund'] = '- -'
        context['last_9_months'] = last_9_months
        context['debt_history'] = last_debts_total
        context['current_year'] = current_year
        context['ipca'] = get_ipca(f'01/01/{current_year}', f'31/12/{current_year}')
        return context


class BillingView(TemplateView):
    template_name = 'pages/billing.html'