from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.forms import InboxAccountForm
from core.models import InboxAccount
from core.session_store import get_current_user


class UpdateInboxAccountView(LoginRequiredMixin, UpdateView):
    model = InboxAccount
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'
    form_class = InboxAccountForm

    def get_form(self, form_class=None):
        return self.get_form_class()(get_current_user(), **self.get_form_kwargs())
