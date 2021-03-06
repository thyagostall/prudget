from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import ModelFormMixin

from core.forms import DebitTransactionForm
from core.models import Transaction


class DebitTransactionViewMixin(LoginRequiredMixin, ModelFormMixin):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    template_name = 'core/transaction_form.html'
    form_class = DebitTransactionForm

    def get_context_data(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'Debit Transaction'
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
