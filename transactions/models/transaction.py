from django.db import models

from budget.models import Expense
from transactions.models import UserModel, Account, Bucket


class Transaction(UserModel):
    description = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    bucket = models.ForeignKey(Bucket, blank=True, null=True, on_delete=models.DO_NOTHING)
    group_id = models.CharField(max_length=50)
    expense = models.ForeignKey(Expense, blank=True, null=True, on_delete=models.DO_NOTHING)
