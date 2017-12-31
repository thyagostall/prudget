from datetime import datetime

from decimal import Decimal
from django.contrib.auth.models import User

from transactions.models import Currency, Account, Transaction, Bucket, BucketValue
from transactions.services import create_group_id


def create_user(username='username', email='any@email.com', password='password'):
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    user.save()
    return user


def create_account(user, name, currency_code):
    currency, _ = Currency.objects.get_or_create(code=currency_code)
    return Account.objects.create(name=name,
                                  currency=currency,
                                  owner=user,
                                  )


def create_bucket(user, name):
    return Bucket.objects.create(name=name,
                                 owner=user
                                 )


def create_bucket_value(bucket, **kwargs):
    amount = kwargs.get('amount', Decimal('400.00'))
    start_period = kwargs.get('start_period', datetime.today())

    return BucketValue.objects.create(bucket=bucket,
                                      amount=amount,
                                      start_period=start_period,
                                      owner=bucket.owner,
                                      )


def create_transaction(user, account, amount=Decimal('129.99'), bucket=None, date=None):
    description = 'Some transaction'
    date = date or datetime.today()
    account = account
    group_id = create_group_id()
    if not bucket:
        bucket = create_bucket(user, 'Some bucket')

    return Transaction.objects.create(description=description,
                                      date=date,
                                      amount=amount,
                                      account=account,
                                      group_id=group_id,
                                      owner=user,
                                      bucket=bucket,
                                      )
