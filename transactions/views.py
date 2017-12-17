from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from transactions.forms import TransactionForm
from transactions.models import Transaction, Account, Bucket, InboxAccount
from transactions.services import create_group_id, get_inbox_account


class LoginView(AuthLoginView):
    template_name = 'transactions/login.html'


class LogoutView(AuthLogoutView):
    template_name = 'transactions/logout.html'


class ListAccountView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['inbox_account'] = self.request.user.inboxaccount_set.first()
        return context


class CreateAccountView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'currency']
    success_url = reverse_lazy('account-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'currency']
    success_url = reverse_lazy('account-list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class UpdateInboxAccountView(LoginRequiredMixin, UpdateView):
    model = InboxAccount
    fields = ['account']
    success_url = reverse_lazy('account-list')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class ListBucketView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class CreateBucketView(LoginRequiredMixin, CreateView):
    model = Bucket
    fields = ['name']
    success_url = reverse_lazy('bucket-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateBucketView(LoginRequiredMixin, UpdateView):
    model = Bucket
    fields = ['name']
    success_url = reverse_lazy('bucket-list')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


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
