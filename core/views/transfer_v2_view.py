from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from core.forms import TransferBucketFormV2
from core.services import transfer_bucket


class FormWithTitleView(FormView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**{**kwargs, 'title': self.title})


class CreateTransferToBucketV2View(LoginRequiredMixin, FormWithTitleView):
    title = 'Transfer to bucket'
    template_name = 'generic_form.html'
    form_class = TransferBucketFormV2
    success_url = reverse_lazy('dashboard')

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        transfer_bucket(self.request.user, **form.cleaned_data)
        return super().form_valid(form)
