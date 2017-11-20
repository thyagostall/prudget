from django.conf.urls import url

from transactions.views import TransactionsView, LoginView, DashboardView

urlpatterns = [
    url(r'^transactions/', TransactionsView.as_view(), name='transactions'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^login/', LoginView.as_view(), name='login'),
]
