from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator

import core.services
from core.forms import DateInput
from core.models import Account, Transaction


class TransferToAccountForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput())
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['destination_account'].queryset = Account.objects.filter(owner=self.user)
        self.fields['account'].queryset = Account.objects.filter(owner=self.user)
        self.fields['date'].initial = datetime.today()

    def save(self, commit=True):
        self.instance.owner = self.user
        self.instance.amount = -abs(self.instance.amount)
        self.instance.save()
        destination_account = Account.objects.get(id=self.data['destination_account'])
        core.services.transfer.transfer_to_account(self.instance, destination_account)
        return super().save(commit)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'account', 'destination_account']
