from django.contrib.auth.models import User
from django.db import models

from core.session_store import get_current_user


class UserManager(models.Manager):
    def get_queryset(self):
        current_user = get_current_user()
        if current_user:
            return super().get_queryset().filter(owner=current_user)
        return super().get_queryset().none()


class UserModel(models.Model):
    all_objects = models.Manager()
    objects = UserManager()

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
        default_manager_name = 'objects'
