class Dashboard:
    _accounts = []
    _transactions = []

    def create(self):
        pass

    def add_transaction(self, transaction):
        self._transactions += [transaction]

    def add_account(self, account):
        self._accounts += [account]

    @property
    def total_balance(self):
        result = 0
        for account in self._accounts:
            result += account.balance
        return result
