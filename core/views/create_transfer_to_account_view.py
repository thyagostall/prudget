from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

import core.services
from core.forms import TransferToAccountForm
from core.models import Transaction


@login_required
def new_transfer_to_account(request):
    form = TransferToAccountForm(request.user, request.POST or None)

    if form.is_valid():
        destination_account = form.cleaned_data.pop('destination_account')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.amount = -abs(transaction.amount)
        transaction.save()

        core.services.transfer.transfer_to_account(transaction, destination_account)
        return redirect('dashboard')

    return render(request, 'generic_form.html', context={
        'title': 'Transfer to Account',
        'form': form,
    })
