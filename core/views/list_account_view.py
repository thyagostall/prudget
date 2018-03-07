from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core import services
from core.models import Account
from core.session_store import get_current_user


class ListAccountView(LoginRequiredMixin, ListView):
    model = Account

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['total'] = services.get_query_set_balance(self.get_queryset())
        context['inbox_account'] = get_current_user().inboxaccount_set.first()
        return context
