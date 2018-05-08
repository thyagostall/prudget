from django import forms
from datetime import datetime, date

from core.forms import DateInput
from core.models import Bucket


class EventValidatorMixin:
    def clean_date(self):
        chosen_date = self.cleaned_data['date']
        if chosen_date > date.today():
            raise forms.ValidationError('A transfer cannot have happened in the future.')

        return chosen_date


class UserFormMixin:
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.queryset = field.queryset.filter(owner=self.user)


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
