from django.views.generic import UpdateView

from core.views.credit_transaction_view_mixin import CreditTransactionMixin


class UpdateCreditTransactionView(CreditTransactionMixin, UpdateView):
    pass
