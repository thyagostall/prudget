from django.views.generic import CreateView

from core.views.debit_transaction_view_mixin import DebitTransactionViewMixin


class CreateDebitTransactionView(DebitTransactionViewMixin, CreateView):
    pass
