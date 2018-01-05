import csv
import datetime
import hashlib
import re
import time
import traceback
from decimal import Decimal
from io import TextIOWrapper

from django.contrib.auth.models import User
from django.db import transaction

from transactions.models import Transaction, Account, Bucket


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


@transaction.atomic
def transfer_to_account(transaction, destination):
    if transaction.amount > 0:
        raise ValueError('Origin transaction amount must be negative')

    group_id = create_group_id(prefix='TRANSF-ACCOUNT')
    transaction.group_id = group_id
    transaction.save()

    transfer_transaction = Transaction.objects.create(description=transaction.description,
                                                      date=transaction.date,
                                                      amount=-transaction.amount,
                                                      account=destination,
                                                      group_id=group_id,
                                                      bucket=transaction.bucket,
                                                      owner=transaction.owner,
                                                      )
    return transaction, transfer_transaction


@transaction.atomic
def transfer_to_user(transaction: Transaction, receiver: User) -> (Transaction, Transaction):
    if transaction.amount > 0:
        raise ValueError('Origin transaction amount must be negative')

    description = transaction.description + ' ({})'

    group_id = create_group_id(prefix='TRANSF-USER')
    transaction.group_id = group_id
    transaction.description = description.format(receiver)
    transaction.save()

    destination_account = get_inbox_account(receiver)

    transfer_transaction = Transaction.objects.create(description=description.format(transaction.owner),
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


def import_file(file, encoding, user):
    file = TextIOWrapper(file, encoding=encoding)
    rows = csv.DictReader(file)
    for row in rows:
        try:
            print(row)
            transaction = Transaction()
            transaction.description = row['description']
            transaction.date = resolve_date(row['date'])
            transaction.amount = resolve_amount(row['income'], row['outcome'])
            transaction.account = resolve_account(row['account'], user)
            transaction.bucket = resolve_bucket(row['bucket'], user)
            transaction.group_id = create_group_id('IMPORT')
            transaction.owner = user
            transaction.save()
        except:
            traceback.print_exc()
            raise


def resolve_date(date):
    return datetime.datetime.strptime(date, '%m/%d/%Y').date()


def resolve_amount(income, outcome):
    chars_to_keep = r'[^\d.]'
    income = re.sub(chars_to_keep, '', income)
    outcome = re.sub(chars_to_keep, '', outcome)
    if income:
        return Decimal(income)
    else:
        return Decimal('-%s' % outcome)


def resolve_account(account_name, user):
    if not account_name:
        return None

    return Account.objects.filter(owner=user).filter(name=account_name).get()


def resolve_bucket(bucket_name, user):
    if not bucket_name:
        return None

    return Bucket.objects.filter(owner=user).filter(name=bucket_name).get()
