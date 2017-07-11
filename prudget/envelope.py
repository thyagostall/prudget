class Envelope:
    def __init__(self, name):
        self._name = name
        self._balance = 0

    def deposit(self, value):
        self._balance += value

    def withdraw(self, value):
        self._balance -= value

    @property
    def balance(self):
        return self._balance

    @property
    def name(self):
        return self._name