from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

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
