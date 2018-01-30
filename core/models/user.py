from django.contrib.auth.models import User
from django.db import models


class UserModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
