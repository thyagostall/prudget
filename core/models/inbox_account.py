from django.db import models

from core.models import UserModel, Account


class InboxAccount(UserModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("owner", "account")
