from django.views.generic import CreateView

from core.views.credit_transaction_view_mixin import CreditTransactionMixin


class CreateCreditTransactionView(CreditTransactionMixin, CreateView):
    pass
