from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import BucketForm


class CreateBucketView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('bucket-list')
    template_name = 'generic_form.html'
    form_class = BucketForm

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Create Bucket'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
