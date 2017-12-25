from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from transactions import services
from transactions.forms import TransactionForm, TransferToUserForm, TransferToAccountForm, BucketForm, UploadFileForm
from transactions.models import Transaction, Account, Bucket, InboxAccount
from transactions.services import create_group_id


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
    template_name = 'transactions/generic_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'currency']
    success_url = reverse_lazy('account-list')
    template_name = 'transactions/generic_form.html'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class UpdateInboxAccountView(LoginRequiredMixin, UpdateView):
    model = InboxAccount
    fields = ['account']
    success_url = reverse_lazy('account-list')
    template_name = 'transactions/generic_form.html'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class ListBucketView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class CreateBucketView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('bucket-list')
    template_name = 'transactions/generic_form.html'
    form_class = BucketForm

    def form_valid(self, form):
        form.instance.owner = self.request.user

        amount_per_month = form.cleaned_data.pop('amount_per_month')
        if amount_per_month:
            form.save()
            services.create_bucket_value(form.instance, amount_per_month)

        return super().form_valid(form)


class UpdateBucketView(LoginRequiredMixin, UpdateView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    template_name = 'transactions/generic_form.html'
    form_class = BucketForm

    def get_initial(self):
        bucket_value = services.get_bucket_value(bucket=self.get_object())
        if bucket_value:
            return {'amount_per_month': bucket_value.amount}

        return None

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        amount_per_month = form.cleaned_data.pop('amount_per_month')
        if amount_per_month:
            services.create_bucket_value(form.instance, amount_per_month)

        return super().form_valid(form)


@login_required
def new_transaction(request):
    form = TransactionForm(request.user, request.POST or None)

    if form.is_valid():
        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user
        transaction.group_id = create_group_id('COMMON')
        transaction.save()
        return redirect('dashboard')

    return render(request, 'transactions/generic_form.html', context={
        'form': form,
    })


@login_required
def new_transfer_to_user(request):
    form = TransferToUserForm(request.user, request.POST or None)

    if form.is_valid():
        destination_username = form.cleaned_data.pop('destination_user')

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user

        user = get_object_or_404(User, username=destination_username)

        services.transfer_to_user(transaction, user)
        return redirect('dashboard')

    return render(request, 'transactions/generic_form.html', context={
        'form': form,
    })


@login_required
def new_transfer_to_account(request):
    form = TransferToAccountForm(request.user, request.POST or None)

    if form.is_valid():
        destination_account = form.cleaned_data.pop('destination_account')
        print(destination_account)

        transaction = Transaction(**form.cleaned_data)
        transaction.owner = request.user

        services.transfer_to_account(transaction, destination_account)
        return redirect('dashboard')

    return render(request, 'transactions/generic_form.html', context={
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

    return render(request, 'transactions/generic_form.html', context={
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


@login_required
def import_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            services.import_file(request.FILES['file'], request.encoding, request.user)
            return HttpResponse('File uploaded')
    else:
        form = UploadFileForm()

    return render(request, 'transactions/upload_form.html', context={
        'form': form
    })
