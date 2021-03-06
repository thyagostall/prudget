from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.models import Account


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name']
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Update Account'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
