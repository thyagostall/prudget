from datetime import datetime

from decimal import Decimal
from django.contrib.auth.models import User

from core.models import Account, Transaction, Bucket


def create_user(username='username', email='any@email.com', password='password'):
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    user.save()
    return user


def create_account(user, name='Checkings'):
    return Account.objects.create(name=name,
                                  owner=user,
                                  )


def create_bucket(user, name='Bucket'):
    return Bucket.objects.create(name=name,
                                 owner=user
                                 )


def create_transaction(user, account=None, amount=Decimal('129.99'), bucket=None, date=None):
    description = 'Some transaction'
    date = date or datetime.today()

    return Transaction.objects.create(description=description,
                                      date=date,
                                      amount=amount,
                                      account=account,
                                      owner=user,
                                      bucket=bucket,
                                      )
