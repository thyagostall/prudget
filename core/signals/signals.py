from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Account, InboxAccount


@receiver(post_save, sender=Account)
def post_save_account(sender, instance, **kwargs):
    current_inbox = InboxAccount.objects.filter(owner=instance.owner).first()
    if not current_inbox:
        InboxAccount.objects.update_or_create(owner=instance.owner, account=instance)
