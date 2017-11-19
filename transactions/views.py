from django.views.generic import FormView

from transactions import transactions
from transactions.forms import TransactionForm
from transactions.models import Transaction


class TransactionsView(FormView):
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

    def get_form(self, form_class=None):
        return TransactionForm(user=self.logged_user)

    def get(self, request, *args, **kwargs):
        self.logged_user = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.logged_user = request.user
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.owner = self.logged_user
        transaction.group_id = transactions.create_group_id('COMMON')
        transaction.save()
        return super().form_valid(form)
