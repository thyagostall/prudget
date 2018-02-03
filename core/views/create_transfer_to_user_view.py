from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

import core.services
from core.forms import TransferToUserForm
from core.models import Transaction


@login_required
def new_transfer_to_user(request):
    form = TransferToUserForm(request.user, request.POST or None)

    if form.is_valid():
        destination_username = form.cleaned_data.pop('destination_user')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.amount = -transaction.amount

        user = get_object_or_404(User, username=destination_username)

        core.services.transfer.transfer_to_user(transaction, user)
        return redirect('dashboard')

    return render(request, 'generic_form.html', context={
        'title': 'Transfer to User',
        'form': form,
    })
