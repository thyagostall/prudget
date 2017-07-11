class Transaction:
    def __init__(self, value, description, account, date, envelope=None):
        self._value = value
        self._description = description
        self._account = account
        self._date = date
        self._envelope = envelope

        self.inject_account(account)
        if envelope:
            self.inject_envelope(envelope)

    def inject_account(self, account):
        raise NotImplementedError

    def inject_envelope(self, envelope):
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
    def inject_account(self, account):
        account.withdraw(self._value)

    def inject_envelope(self, envelope):
        envelope.withdraw(self._value)


class CreditTransaction(Transaction):
    def inject_account(self, account):
        account.deposit(self._value)

    def inject_envelope(self, envelope):
        envelope.deposit(self._value)
