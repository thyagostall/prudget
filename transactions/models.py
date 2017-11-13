from django.contrib.auth.models import User
from django.db import models


class UserModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class Currency(UserModel):
    code = models.CharField(max_length=5)


class Account(UserModel):
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency)


class Bucket(UserModel):
    name = models.CharField(max_length=30)


class Transaction(UserModel):
    description = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    bucket = models.ForeignKey(Bucket)


class Transfer(UserModel):
    source = models.ForeignKey(Account, related_name='+')
    destination = models.ForeignKey(Account, related_name='+')
    amount_source = models.DecimalField(max_digits=10, decimal_places=2)
    amount_destination = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
