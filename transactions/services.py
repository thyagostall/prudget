import hashlib
import time

from transactions.models import Transaction


def create_group_id(prefix=''):
    if prefix:
        prefix += '-'

    microseconds = int(time.time() * 100000)
    microseconds = str(microseconds)
    microseconds = microseconds.encode('utf-8')

    digest = hashlib.md5()
    digest.update(microseconds)
    group_id = digest.hexdigest()
    return prefix + group_id.upper()


def transfer_to_account(transaction, destination):
    group_id = create_group_id(prefix='TRANSF-ACCOUNT-')
    transaction.group_id = group_id
    transaction.save()

    transfer_transaction = Transaction.objects.create(description=transaction.description,
                                                      date=transaction.date,
                                                      amount=transaction.amount,
                                                      account=destination,
                                                      group_id=group_id,
                                                      owner=transaction.owner,
                                                      )
    return transaction, transfer_transaction