from django import forms
from django.core.validators import MinValueValidator

import core.services
from core.forms import TransactionForm
from core.models import Bucket, Transaction


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
