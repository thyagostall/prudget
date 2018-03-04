from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

import core.services
from core.forms import TransferToAccountForm
from core.models import Transaction
from core.session_store import get_current_user


@login_required
def new_transfer_to_account(request):
    form = TransferToAccountForm(get_current_user(), request.POST or None)

    if form.is_valid():
        destination_account = form.cleaned_data.pop('destination_account')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = get_current_user()
        transaction.amount = -abs(transaction.amount)
        transaction.save()

        core.services.transfer.transfer_to_account(transaction, destination_account)
        return redirect('dashboard')

    return render(request, 'generic_form.html', context={
        'title': 'Transfer to Account',
        'form': form,
    })
