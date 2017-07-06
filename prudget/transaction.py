class Transaction:
    def __init__(self, value, description, account, today):
        self._value = value
        self._description = description
        self._account = account
        self._today = today

        self.inject(account)

    def inject(self, account):
        raise NotImplementedError

    @property
    def value(self):
        return self._value


class DebitTransaction(Transaction):
    def inject(self, account):
        account.withdraw(self._value)


class CreditTransaction(Transaction):
    def inject(self, account):
        account.deposit(self._value)
