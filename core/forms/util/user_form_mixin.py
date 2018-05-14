from django import forms


class UserFormMixin:
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.queryset = field.queryset.filter(owner=self.user)
