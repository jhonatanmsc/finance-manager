from datetime import datetime

from django import urls
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from credits.models import Credit
from debts.models import Debt
from goals.models import Goal, Contribution
from parameters.models import Parameter
from src.enums import RecurrenceEnum, PaymentMethod
from src.utils import real_currency, get_last_9_months, get_ipca, get_min_salary


class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect(urls.reverse('admin:login'))
        current_month = datetime.now().month
        current_year = datetime.now().year
        recurrence_debts = (
            Debt.objects
            .filter(user=self.request.user)
            .exclude(
                Q(recurrence=RecurrenceEnum.NONE) | Q(payment_method__iexact=PaymentMethod.CASH.value)
            )
        )
        extra_debts = (
            Debt.objects
            .filter(
                user=self.request.user,
                created_at__month=current_month,
                created_at__year=current_year
            )
            .exclude(Q(recurrence=RecurrenceEnum.NONE) | Q(payment_method__iexact=PaymentMethod.CASH.value))
        )

        debts = recurrence_debts.union(extra_debts)
        debts = sum([debt.value for debt in debts])
        emergency_fund = Parameter.objects.filter(user=self.request.user, name='reserva_1').first()
        emergency_fund = emergency_fund.index
        goal = Goal.objects.filter(user=self.request.user, title="Reserva de Médio prazo").first()
        credit_list = Credit.objects.filter(user=self.request.user)
        total_credit = sum([cred.limit for cred in credit_list])

        context['data'] = [
            {"title": "Gasto mensal esperado", "total": real_currency(debts), "variation": 0},
            {"title": "Reserva de emergência", "total": real_currency(debts * emergency_fund), "variation": 0},
            {"title": "Reserva médio prazo", "total": real_currency(goal.value), "variation": 0},
            {"title": "Reserva longo prazo", "total": '- -', "variation": 0},
            {"title": "Total de crédito", "total": real_currency(total_credit), "variation": 0},
        ]
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
        contrib_dict = {g.title: {'id': g.id, 'budget': g.value, 'amount': 0, 'status': 'aguardando'} for g in goals}
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


class GoalDetailView(TemplateView):
    template_name = "pages/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect(urls.reverse('admin:login'))
        goal = Goal.objects.filter(id=kwargs['id']).first()
        context['goal'] = goal
        contributions = goal.contributions.filter(user=self.request.user)
        groups = {}
        for contribution in contributions:
            if contribution.group_name not in groups:
                groups[contribution.group_name] = contribution.value
            else:
                groups[contribution.group_name] += contribution.value
        context['groups'] = groups
        return context