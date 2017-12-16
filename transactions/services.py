import hashlib
import time

from django.contrib.auth.models import User

from transactions.models import Transaction, Account


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


def transfer_to_user(transaction: Transaction, receiver: User) -> (Transaction, Transaction):
    group_id = create_group_id(prefix='TRANSF-USER')
    transaction.group_id = group_id
    transaction.save()

    destination_account = get_inbox_account(receiver)

    transfer_transaction = Transaction.objects.create(description=transaction.description,
                                                      date=transaction.date,
                                                      amount=-transaction.amount,
                                                      account=destination_account,
                                                      group_id=group_id,
                                                      owner=receiver)

    return transaction, transfer_transaction


def get_inbox_account(user: User) -> Account:
    result = user.inboxaccount_set.first()
    if not result:
        raise Exception("This user doesn't have an associated inbox account")

    return result.account
