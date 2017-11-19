from django.conf.urls import url

from transactions.views import TransactionsView

urlpatterns = [
    url(r'^transactions/', TransactionsView.as_view(), name='transactions'),
]
