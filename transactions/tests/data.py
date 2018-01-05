from datetime import datetime

from decimal import Decimal
from django.contrib.auth.models import User

from transactions.models import Account, Transaction, Bucket
from transactions.services import create_group_id


def create_user(username='username', email='any@email.com', password='password'):
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    user.save()
    return user


def create_account(user, name):
    return Account.objects.create(name=name,
                                  owner=user,
                                  )


def create_bucket(user, name):
    return Bucket.objects.create(name=name,
                                 owner=user
                                 )


def create_transaction(user, account=None, amount=Decimal('129.99'), bucket=None, date=None):
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
