from django import forms
from django.core.validators import MinValueValidator

from core.forms import TransactionForm
from core.models import Account, Transaction


class TransferToAccountForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['destination_account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_account']
