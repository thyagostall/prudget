from datetime import datetime

from django import forms

from transactions.models import Bucket, Account, Transaction


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), initial=datetime.today())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bucket'].queryset = Bucket.objects.filter(owner=user)
        self.fields['account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account']
