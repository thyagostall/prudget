from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core import services
from core.models import Account


class ListAccountView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['total'] = services.get_query_set_balance(self.get_queryset())
        context['inbox_account'] = self.request.user.inboxaccount_set.first()
        return context
