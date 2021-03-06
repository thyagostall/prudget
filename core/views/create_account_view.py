from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.models import Account


class CreateAccountView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name']
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Create Account'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
