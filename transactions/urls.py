from django.conf.urls import url

from transactions import views
from transactions.views import TransactionsView, LoginView, AccountListView

urlpatterns = [
    url(r'^transactions/', TransactionsView.as_view(), name='transactions'),
    url(r'^account-list/', AccountListView.as_view(), name='account_list'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
]
