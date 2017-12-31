from django.forms import ModelForm

from budget.models import Expense


class ExpenseForm(ModelForm):
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(**kwargs)

    def clean(self):
        self.instance.owner = self.user

    class Meta:
        model = Expense
        fields = ['description',
                  'amount',
                  'estimated',
                  'due_day',
                  'due_weekday',
                  'periodicity',
                  ]
