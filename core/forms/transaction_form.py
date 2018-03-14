from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator

from core.forms import DateInput
from core.models import Bucket, Account, Transaction


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), initial=datetime.today())
    amount = forms.DecimalField(validators=[MinValueValidator(0)])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = user
        self.fields['bucket'].queryset = Bucket.objects.all()
        self.fields['account'].queryset = Account.objects.all()

    def save(self, commit=True):
        self.instance.owner = self.owner
        return super().save(commit=commit)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account']
