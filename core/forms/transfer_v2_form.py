from django import forms
from datetime import datetime

from core.forms import DateInput
from core.forms.util.event_validator_mixin import EventValidatorMixin
from core.forms.util.user_form_mixin import UserFormMixin
from core.models import Bucket


class TransferBucketFormV2(UserFormMixin, EventValidatorMixin, forms.Form):
    description = forms.CharField(max_length=50)
    date = forms.DateField(widget=DateInput(), initial=datetime.today())
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    source_bucket = forms.ModelChoiceField(Bucket.objects.all())
    destination_bucket = forms.ModelChoiceField(Bucket.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        source_bucket = cleaned_data.get('source_bucket')
        destination_bucket = cleaned_data.get('destination_bucket')

        if source_bucket == destination_bucket:
            raise forms.ValidationError('Source and destination buckets must differ.')

        return cleaned_data
