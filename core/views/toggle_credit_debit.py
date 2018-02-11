from django.http import Http404
from django.shortcuts import redirect, get_object_or_404

from core import services
from core.models import Transaction


def toggle_credit_debit(request, pk):
    if not request.POST:
        raise Http404()

    transaction = get_object_or_404(Transaction, pk=pk)
    services.toggle_credit_debit_and_save(transaction)
    return redirect('dashboard')
