import datetime
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
        bucket_value_amount = self.get_bucket_value()
        current_month = datetime.date.today().month

        result = self.transaction_set \
            .filter(date__month=current_month) \
            .aggregate(balance=Sum('amount'))

        return bucket_value_amount + (result['balance'] or Decimal(0))

    def get_bucket_value(self):
        bucket_value = BucketValue.objects \
            .filter(bucket=self) \
            .order_by('-start_period') \
            .first()

        if bucket_value:
            return bucket_value.amount
        else:
            return Decimal(0)

    def __str__(self):
        return self.name


class BucketValue(UserModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_period = models.DateField()
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
