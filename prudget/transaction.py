class Transaction:
    def __init__(self, value, description, account, date):
        self._value = value
        self._description = description
        self._account = account
        self._date = date

        self.inject(account)

    def inject(self, account):
        raise NotImplementedError

    @property
    def value(self):
        return self._value

    @property
    def description(self):
        return self._description

    @property
    def account(self):
        return self._account

    @property
    def date(self):
        return self._date


class DebitTransaction(Transaction):
    def inject(self, account):
        account.withdraw(self._value)


class CreditTransaction(Transaction):
    def inject(self, account):
        account.deposit(self._value)
