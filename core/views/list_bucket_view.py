from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core import services
from core.models import Bucket
from core.session_store import get_current_user


class ListBucketView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        total = services.get_query_set_balance(self.get_queryset())
        return {**context_data, 'bucket_total': total}

    def get_queryset(self):
        return super().get_queryset().filter(owner=get_current_user())
