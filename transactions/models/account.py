from decimal import Decimal

from django.db import models
from django.db.models import Sum

from transactions.models import UserModel, Currency


class Account(UserModel):
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)

    def balance(self):
        result = self.transaction_set.aggregate(balance=Sum('amount'))
        return result['balance'] or Decimal(0)

    def __str__(self):
        return self.name
