from datetime import datetime

from django import urls
from django.shortcuts import redirect
from django.views.generic import TemplateView

from debts.models import Debt
from goals.models import Goal, Contribution
from parameters.models import Parameter
from src.enums import RecurrenceEnum
from src.utils import real_currency, get_last_9_months, get_ipca, get_min_salary


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
        accounting_fee = Parameter.objects.filter(user=self.request.user, name='contabilidade').first()
        accounting_fee = float(accounting_fee.index)
        goal = Goal.objects.filter(user=self.request.user, title="Reserva de Médio prazo").first()
        context['sidebar_option'] = 'dashboard'
        context['debts'] = real_currency(debts)
        context['emergency_fund'] = real_currency(debts * emergency_fund)
        context['mid_fund'] = real_currency(goal.value)
        context['long_fund'] = '- -'
        context['last_9_months'] = last_9_months
        context['debt_history'] = last_debts_total
        context['current_year'] = current_year
        context['ipca'] = get_ipca(f'01/01/{current_year}', f'31/12/{current_year}')
        min_salary = get_min_salary(f'01/01/{current_year}', f'31/12/{current_year}')
        context['min_salary'] = real_currency(min_salary)
        context['accounting_fee'] = real_currency(min_salary * accounting_fee)
        return context


class BillingView(TemplateView):
    template_name = 'pages/billing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect(urls.reverse('admin:login'))

        context['sidebar_option'] = 'billing'
        return context


class TableView(TemplateView):
    template_name = 'pages/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect(urls.reverse('admin:login'))

        goals = Goal.objects.filter(user=self.request.user)
        contributions = Contribution.objects.filter(goal__user=self.request.user)
        contrib_dict = {g.title: {'budget': g.value, 'amount': 0, 'status': 'aguardando'} for g in goals}
        for contribution in contributions:
            contrib_dict[contribution.goal.title]['amount'] += contribution.value * contribution.quantity
            if contribution.goal.canceled_at is None and contribution.goal.concluded_at is None:
                contrib_dict[contribution.goal.title]['status'] = 'ativo'
            elif contribution.goal.canceled_at is not None:
                contrib_dict[contribution.goal.title]['status'] = 'cancelado'
            elif contribution.goal.concluded_at is not None:
                contrib_dict[contribution.goal.title]['status'] = 'concluído'

        for con in contrib_dict:
            contrib = contrib_dict[con]
            if contrib['amount'] <= 0:
                contrib['completion'] = 0
            else:
                contrib['completion'] = '%.2f' % ((contrib['amount'] / contrib['budget']) * 100)
            contrib['budget'] = real_currency(contrib['budget'])
            contrib['amount'] = real_currency(contrib['amount'])

            contrib_dict[con] = contrib


        context['sidebar_option'] = 'table'
        context['goals'] = goals
        context['contributions'] = contrib_dict
        return context


class VirtualView(TemplateView):
    template_name = 'pages/virtual-reality.html'
