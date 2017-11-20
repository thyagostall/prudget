from transactions.models import Transaction
from transactions.transactions import create_group_id


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
