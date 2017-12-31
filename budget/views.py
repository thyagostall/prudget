from decimal import Decimal
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from budget import services
from budget.forms import ExpenseForm
from budget.models import Expense


class CreateExpenseView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('budget:expense-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateExpenseView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('budget:expense-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ListExpenseView(ListView):
    model = Expense

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        result = super().get_context_data(object_list=object_list, **kwargs)
        expense_queryset = self.get_queryset()

        total_expenses = services.sum_expenses_amounts(expense_queryset)
        result['total_expenses'] = total_expenses

        result['buckets'] = buckets_query_set = services.get_bucket_queryset(self.request.user)

        total_buckets = services.sum_bucket_balance(buckets_query_set)
        result['total_buckets'] = total_buckets

        total_income = Decimal(0)
        result['profit_or_loss'] = services.calculate_profit_or_loss(total_income, total_buckets, total_expenses)

        return result
