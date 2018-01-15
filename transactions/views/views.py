from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.edit import ModelFormMixin

from transactions import services
from transactions.forms import TransactionForm, TransferToUserForm, TransferToAccountForm, BucketForm, InboxAccountForm
from transactions.forms.forms import TransferToBucketForm, DebitTransactionForm
from transactions.models import Transaction, Account, Bucket, InboxAccount


class LoginView(AuthLoginView):
    template_name = 'transactions/login.html'


class LogoutView(AuthLogoutView):
    template_name = 'transactions/logout.html'


class ListAccountView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['inbox_account'] = self.request.user.inboxaccount_set.first()
        return context


class CreateAccountView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name']
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name']
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class UpdateInboxAccountView(LoginRequiredMixin, UpdateView):
    model = InboxAccount
    success_url = reverse_lazy('account-list')
    template_name = 'generic_form.html'
    form_class = InboxAccountForm

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ListBucketView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        total = services.get_query_set_balance(self.get_queryset())
        return {**context_data, 'total': total}

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CreateBucketView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('bucket-list')
    template_name = 'generic_form.html'
    form_class = BucketForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateBucketView(LoginRequiredMixin, UpdateView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    template_name = 'generic_form.html'
    form_class = BucketForm

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CreateTransferToBucketView(LoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    template_name = 'generic_form.html'
    form_class = TransferToBucketForm

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class DebitTransactionViewMixin(LoginRequiredMixin, ModelFormMixin):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    template_name = 'generic_form.html'
    form_class = DebitTransactionForm

    def get_context_data(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'Debit Transaction'
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CreateDebitTransactionView(DebitTransactionViewMixin, CreateView):
    pass


class UpdateDebitTransactionView(DebitTransactionViewMixin, UpdateView):
    def get_object(self, queryset=None):
        result = super().get_object(queryset)
        result.amount = abs(result.amount)
        return result


class CreditTransactionView(LoginRequiredMixin, ModelFormMixin):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    template_name = 'generic_form.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'Credit Transaction'
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        return self.get_form_class()(self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CreateCreditTransactionView(CreditTransactionView, CreateView):
    pass


class UpdateCreditTransactionView(CreditTransactionView, UpdateView):
    pass


@login_required
def new_transfer_to_user(request):
    form = TransferToUserForm(request.user, request.POST or None)

    if form.is_valid():
        destination_username = form.cleaned_data.pop('destination_user')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.amount = -transaction.amount

        user = get_object_or_404(User, username=destination_username)

        services.transfer_to_user(transaction, user)
        return redirect('dashboard')

    return render(request, 'generic_form.html', context={
        'form': form,
    })


@login_required
def new_transfer_to_account(request):
    form = TransferToAccountForm(request.user, request.POST or None)

    if form.is_valid():
        destination_account = form.cleaned_data.pop('destination_account')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.amount = -transaction.amount

        services.transfer_to_account(transaction, destination_account)
        return redirect('dashboard')

    return render(request, 'generic_form.html', context={
        'form': form,
    })


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction.amount > Decimal('0'):
        return redirect('update-credit-transaction', pk=pk)
    else:
        return redirect('update-debit-transaction', pk=pk)


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(owner=request.user).order_by('-date', '-id')
    accounts = Account.objects.filter(owner=request.user)

    context = {
        'transactions': transactions,
        'accounts': accounts,
    }
    return render(request, 'transactions/dashboard.html', context=context)
