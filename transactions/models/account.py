from decimal import Decimal

from django.db import models
from django.db.models import Sum

from transactions.models import UserModel


class Account(UserModel):
    name = models.CharField(max_length=30)

    def balance(self):
        result = self.transaction_set.aggregate(balance=Sum('amount'))
        return result['balance'] or Decimal(0)

    def __str__(self):
        return self.name
