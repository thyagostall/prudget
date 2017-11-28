from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import render

from transactions.forms import TransactionForm
from transactions.models import Transaction, Account
from transactions.transactions import create_group_id


class LoginView(AuthLoginView):
    template_name = 'transactions/login.html'


class LogoutView(AuthLogoutView):
    template_name = 'transactions/logout.html'


@login_required
def dashboard(request):
    form = TransactionForm(request.user, request.POST or None)

    if form.is_valid():
        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.group_id = create_group_id('COMMON')
        transaction.save()

    transactions = Transaction.objects.filter(owner=request.user).order_by('-id')
    accounts = Account.objects.filter(owner=request.user)

    context = {
        'transactions': transactions,
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'transactions/dashboard.html', context=context)
