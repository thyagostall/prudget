from django.db.models import Sum

from transactions.models import Transaction
from transactions.transaction import create_group_id


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


def get_account_balance(account):
    result = account.transaction_set.aggregate(balance=Sum('amount'))
    return result['balance']
