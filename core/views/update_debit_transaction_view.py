from django.views.generic import UpdateView

from core.views.debit_transaction_view_mixin import DebitTransactionViewMixin


class UpdateDebitTransactionView(DebitTransactionViewMixin, UpdateView):
    def get_object(self, queryset=None):
        result = super().get_object(queryset)
        result.amount = abs(result.amount)
        return result
