from django.db import transaction

from core.models import Transaction
from core.models.transaction_link import TransactionLink


class TransferException(Exception):
    pass


@transaction.atomic
def transfer_bucket(owner, *, description, date, amount, source_bucket, destination_bucket):
    if amount <= 0:
        raise TransferException("Amount must be positive")

    if source_bucket == destination_bucket:
        raise TransferException("Source and destination buckets must differ")

    source_amount = amount * -1
    destination_amount = amount

    source_transaction = Transaction.objects.create(
        description=description,
        date=date,
        amount=source_amount,
        bucket=source_bucket,
        owner=owner,
    )
    destination_transaction = Transaction.objects.create(
        description=description,
        date=date,
        amount=destination_amount,
        bucket=destination_bucket,
        owner=owner,
    )

    return TransactionLink.objects.create(
        source_transaction=source_transaction,
        destination_transaction=destination_transaction,
        type=TransactionLink.TRANSFER_BUCKET,
    )
