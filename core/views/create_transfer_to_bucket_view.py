from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms.forms import TransferToBucketForm
from core.models import Transaction


class CreateTransferToBucketView(LoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    template_name = 'generic_form.html'
    form_class = TransferToBucketForm

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Transfer to Bucket'
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
