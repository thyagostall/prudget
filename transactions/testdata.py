from datetime import datetime

from decimal import Decimal
from django.contrib.auth.models import User

from transactions.models import Currency, Account, Transaction
from transactions.services import create_group_id


def create_user(username='username', email='any@email.com', password='password'):
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    user.save()
    return user


def create_account(user, account_name, currency_code):
    currency, _ = Currency.objects.get_or_create(code=currency_code)
    return Account.objects.create(name=account_name,
                                  currency=currency,
                                  owner=user,
                                  )


def create_transaction(user, source, amount=Decimal('129.99')):
    description = 'Some transaction'
    date = datetime.today()
    account = source
    group_id = create_group_id()

    return Transaction.objects.create(description=description,
                                      date=date,
                                      amount=amount,
                                      account=account,
                                      group_id=group_id,
                                      owner=user,
                                      )
