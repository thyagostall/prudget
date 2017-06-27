from functools import reduce

class Dashboard:
    def __init__(self):
        self._accounts = []
        self._transactions = []

    def add_transaction(self, transaction):
        self._transactions += [transaction]

    def add_account(self, account):
        self._accounts += [account]

    @property
    def total_balance(self):
        return reduce(lambda previous, account: account.balance + previous, self._accounts, 0)

    @property
    def transactions(self):
        return self._transactions

    @property
    def accounts(self):
        return self._accounts
