import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class UserModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class Currency(models.Model):
    code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code


class Account(UserModel):
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)

    def balance(self):
        result = self.transaction_set.aggregate(balance=Sum('amount'))
        return result['balance'] or Decimal(0)

    def __str__(self):
        return self.name


class Bucket(UserModel):
    name = models.CharField(max_length=30)

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


class Transaction(UserModel):
    description = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    bucket = models.ForeignKey(Bucket, blank=True, null=True, on_delete=models.DO_NOTHING)
    group_id = models.CharField(max_length=50)


class InboxAccount(UserModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("owner", "account")
