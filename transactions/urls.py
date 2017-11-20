from django.conf.urls import url

from transactions.views import TransactionsView, LoginView

urlpatterns = [
    url(r'^transactions/', TransactionsView.as_view(), name='transactions'),
    url(r'^login/', LoginView.as_view(), name='login'),
]
