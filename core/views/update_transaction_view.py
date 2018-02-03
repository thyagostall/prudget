from _pydecimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from core.models import Transaction


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction.amount > Decimal('0'):
        return redirect('update-credit-transaction', pk=pk)
    else:
        return redirect('update-debit-transaction', pk=pk)
