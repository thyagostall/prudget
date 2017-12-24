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


class TransferToUserForm(TransactionForm):
    destination_user = forms.CharField(max_length=150)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_user']


class TransferToAccountForm(TransactionForm):
    destination_account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['destination_account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_account']


class BucketForm(forms.ModelForm):
    amount_per_month = forms.DecimalField(min_value=0, decimal_places=True)

    class Meta:
        model = Bucket
        fields = ['name', 'amount_per_month']
