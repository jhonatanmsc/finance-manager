from django.contrib.auth.decorators import login_required
from django.urls import path

from dashboard.views import DashboardView, BillingView, TableView, VirtualView

urlpatterns = [
    path('', login_required(DashboardView.as_view()), name='dashboard'),
    path('billing', login_required(BillingView.as_view()), name='billing'),
    path('tables', login_required(TableView.as_view()), name='tables'),
]