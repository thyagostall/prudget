from decimal import Decimal

from django.db import models
from django.db.models import Sum

from transactions.models import UserModel


class Bucket(UserModel):
    name = models.CharField(max_length=30)
    show_balance = models.BooleanField(default=False)

    def balance(self):
        return self.get_bucket_balance()

    def get_bucket_balance(self):
        result = self.transaction_set.aggregate(balance=Sum('amount'))
        return result['balance'] or Decimal(0)

    def __str__(self):
        return self.name
