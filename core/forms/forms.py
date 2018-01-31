from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator

import core.services.transfer
from core import services
from core.models import Bucket, Account, Transaction, InboxAccount


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
    amount = forms.DecimalField(validators=[MinValueValidator(0)])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = user
        self.fields['bucket'].queryset = Bucket.objects.filter(owner=self.owner)
        self.fields['account'].queryset = Account.objects.filter(owner=self.owner)

    def save(self, commit=True):
        self.instance.owner = self.owner
        return super().save(commit=commit)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account']


class DebitTransactionForm(TransactionForm):
    def save(self, commit=True):
        self.instance.amount = -abs(self.instance.amount)
        return super().save(commit=commit)


class TransferToUserForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_user = forms.CharField(max_length=150)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_user']


class TransferToAccountForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['destination_account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_account']


class TransferToBucketForm(TransactionForm):
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    destination_bucket = forms.ModelChoiceField(queryset=Bucket.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user
        self.fields['destination_bucket'].queryset = Bucket.objects.filter(owner=self.user)

    def save(self, commit=True):
        self.instance.owner = self.user
        destination_bucket = Bucket.objects.get(id=self.data['destination_bucket'])
        core.services.transfer.transfer_to_bucket(self.instance, destination_bucket)
        return super().save(commit)

    class Meta:
        model = Transaction
        fields = ['description', 'date', 'amount', 'bucket', 'account', 'destination_bucket']


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name']