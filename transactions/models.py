from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=5)


class Account(models.Model):
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency)


class Bucket(models.Model):
    name = models.CharField(max_length=30)


class Transaction(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    bucket = models.ForeignKey(Bucket)


class Transfer(models.Model):
    source = models.ForeignKey(Account, related_name='+')
    destination = models.ForeignKey(Account, related_name='+')
    amount_source = models.DecimalField(max_digits=10, decimal_places=2)
    amount_destination = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
