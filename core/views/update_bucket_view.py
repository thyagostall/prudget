from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.forms import BucketForm
from core.models import Bucket
from core.session_store import get_current_user


class UpdateBucketView(LoginRequiredMixin, UpdateView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    template_name = 'generic_form.html'
    form_class = BucketForm

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Update Bucket'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(owner=get_current_user())
