from django import forms

from core.models import Bucket


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name']
