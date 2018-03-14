from django import forms

from core.models import Account, InboxAccount


class InboxAccountForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.all()

    class Meta:
        model = InboxAccount
        fields = ['account']
