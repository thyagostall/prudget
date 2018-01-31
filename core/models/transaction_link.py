from django.db import models

from core.models import Transaction


class TransactionLink(models.Model):
    TRANSFER_USER = 'TU'
    TRANSFER_ACCOUNT = 'TA'
    TRANSFER_BUCKET = 'TB'

    LINK_TYPE = (
        (TRANSFER_USER, 'Transfer between users'),
        (TRANSFER_ACCOUNT, 'Transfer between accounts'),
        (TRANSFER_BUCKET, 'Transfer between buckets'),
    )

    type = models.CharField(max_length=2, choices=LINK_TYPE)
    source_transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING, related_name='source_transaction')
    destination_transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING,
                                                related_name='destination_transaction')
