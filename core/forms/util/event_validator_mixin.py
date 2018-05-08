from datetime import date

from django import forms


class EventValidatorMixin:
    def clean_date(self):
        chosen_date = self.cleaned_data['date']
        if chosen_date > date.today():
            raise forms.ValidationError('A transfer cannot have happened in the future.')

        return chosen_date
