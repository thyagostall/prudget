from decimal import Decimal

class Account:
    def __init__(self):
        self._balance = Decimal(0)

    @property
    def balance(self):
        return self._balance

    def deposit(self, value):
        self._balance += value

    def withdraw(self, value):
        self._balance -= value
