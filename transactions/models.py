from django.contrib.auth.models import User
from django.db import models


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
    currency = models.ForeignKey(Currency)

    def __str__(self):
        return '%s (%s)' % (self.name, self.currency)


class Bucket(UserModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Transaction(UserModel):
    description = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    bucket = models.ForeignKey(Bucket, blank=True, null=True)
    group_id = models.CharField(max_length=50)
