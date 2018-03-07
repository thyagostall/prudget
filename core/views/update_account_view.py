from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.models import Account
from core.session_store import get_current_user


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name']
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Update Account'
        return super().get_context_data(**kwargs)
