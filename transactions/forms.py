from datetime import datetime

from django import forms

from transactions.models import Bucket, Account, Transaction


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), initial=datetime.today())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_user = user
        self.fields['bucket'].queryset = Bucket.objects.filter(owner=self.logged_user)
        self.fields['account'].queryset = Account.objects.filter(owner=self.logged_user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account']
