from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import render, redirect, get_object_or_404

from transactions.forms import TransactionForm
from transactions.models import Transaction, Account
from transactions.services import create_group_id


class LoginView(AuthLoginView):
    template_name = 'transactions/login.html'


class LogoutView(AuthLogoutView):
    template_name = 'transactions/logout.html'


@login_required
def new_transaction(request):
    form = TransactionForm(request.user, request.POST or None)

    if form.is_valid():
        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.group_id = create_group_id('COMMON')
        transaction.save()
        return redirect('dashboard')

    return render(request, 'transactions/transaction.html', context={
        'form': form,
    })


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(request.user, request.POST or None, instance=transaction)

    if form.is_valid():
        transaction = form.instance
        transaction.save()
        return redirect('dashboard')

    return render(request, 'transactions/transaction.html', context={
        'form': form,
    })


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(owner=request.user).order_by('-date')
    accounts = Account.objects.filter(owner=request.user)

    context = {
        'transactions': transactions,
        'accounts': accounts,
    }
    return render(request, 'transactions/dashboard.html', context=context)
