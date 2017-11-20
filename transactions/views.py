from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views.generic import FormView
from django.views.generic import TemplateView

from transactions import transactions
from transactions.forms import TransactionForm
from transactions.models import Transaction, Account


class TransactionsView(LoginRequiredMixin, FormView):
    login_url = '/finance/login/'

    form_class = TransactionForm
    template_name = 'transactions/transactions.html'
    success_url = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logged_user = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(owner=self.logged_user).order_by('-id')
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'user': self.logged_user
        })
        return form_kwargs

    def form_valid(self, form):
        print('save')
        transaction = form.save(commit=False)
        transaction.owner = self.logged_user
        transaction.group_id = transactions.create_group_id('COMMON')
        transaction.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.logged_user = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.logged_user = request.user
        return super().post(request, *args, **kwargs)


class LoginView(AuthLoginView):
    template_name = 'transactions/login.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/finance/login/'
    template_name = 'transactions/dashboard.html'

    def get_context_data(self, **kwargs):
        accounts = Account.objects.filter(owner=self.request.user)
        return dict(accounts=accounts)
