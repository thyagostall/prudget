from django import forms
from django.core.validators import MinValueValidator

from core.forms import TransactionForm
from core.models import Transaction


class TransferToUserForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_user = forms.CharField(max_length=150)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_user']
