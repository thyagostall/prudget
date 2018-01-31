from django.db import transaction

from core.models import Transaction
from core.models.transaction_link import TransactionLink


@transaction.atomic
def transfer_to_bucket(source_transaction, destination):
    if source_transaction.amount > 0:
        raise ValueError('Origin transaction amount must be negative')

    destination_transaction = Transaction.objects.create(description=source_transaction.description,
                                                         date=source_transaction.date,
                                                         amount=-source_transaction.amount,
                                                         account=source_transaction.account,
                                                         bucket=destination,
                                                         owner=source_transaction.owner,
                                                         )
    transaction_link = TransactionLink.objects.create(type=TransactionLink.TRANSFER_BUCKET,
                                                      source_transaction=source_transaction,
                                                      destination_transaction=destination_transaction
                                                      )
    return transaction_link


@transaction.atomic
def transfer_to_account(source_transaction, destination):
    if source_transaction.amount > 0:
        raise ValueError('Origin transaction amount must be negative')

    destination_transaction = Transaction.objects.create(description=source_transaction.description,
                                                         date=source_transaction.date,
                                                         amount=-source_transaction.amount,
                                                         account=destination,
                                                         bucket=source_transaction.bucket,
                                                         owner=source_transaction.owner,
                                                         )
    transaction_link = TransactionLink.objects.create(type=TransactionLink.TRANSFER_ACCOUNT,
                                                      source_transaction=source_transaction,
                                                      destination_transaction=destination_transaction
                                                      )
    return transaction_link


@transaction.atomic
def transfer_to_user(source_transaction, receiver):
    if source_transaction.amount > 0:
        raise ValueError('Origin transaction amount must be negative')

    destination_account = get_inbox_account(receiver)
    destination_transaction = Transaction.objects.create(description=source_transaction.description,
                                                         date=source_transaction.date,
                                                         amount=-source_transaction.amount,
                                                         account=destination_account,
                                                         owner=receiver
                                                         )
    transaction_link = TransactionLink.objects.create(type=TransactionLink.TRANSFER_USER,
                                                      source_transaction=source_transaction,
                                                      destination_transaction=destination_transaction
                                                      )
    return transaction_link


def get_inbox_account(user):
    result = user.inboxaccount_set.first()
    if not result:
        raise Exception("This user doesn't have an associated inbox account")

    return result.account
