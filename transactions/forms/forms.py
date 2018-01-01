from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator

from transactions.models import Bucket, Account, Transaction, InboxAccount, Expense


class DateInput(forms.DateInput):
    input_type = 'date'


class InboxAccountForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = InboxAccount
        fields = ['account']


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), initial=datetime.today())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bucket'].queryset = Bucket.objects.filter(owner=user)
        self.fields['account'].queryset = Account.objects.filter(owner=user)
        self.fields['expense'].queryset = Expense.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'expense']


class TransferToUserForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_user = forms.CharField(max_length=150)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_user', 'expense']


class TransferToAccountForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['destination_account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_account', 'expense']


class BucketForm(forms.ModelForm):
    amount_per_month = forms.DecimalField(min_value=0, decimal_places=True, required=False)
    show_balance = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Bucket
        fields = ['name', 'amount_per_month', 'show_balance']


class UploadFileForm(forms.Form):
    file = forms.FileField()
