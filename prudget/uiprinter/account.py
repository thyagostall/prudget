from prudget.uiprinter.base import UIPrinter


class UIAccountPrinter(UIPrinter):
    ACCOUNT_LENGTH = 25
    CURRENCY_LENGTH = 10

    LINE_FORMAT = '| {: <{account_length}} | {: >{currency_length}.2f} |'

    def __init__(self, accounts):
        super().__init__()
        self._accounts = accounts

    @classmethod
    def _print_account(cls, account, length):
        return cls.LINE_FORMAT.format(
            account.name,
            account.balance,
            account_length=length,
            currency_length=cls.CURRENCY_LENGTH
        )

    def _get_line_length(self):
        line = self.LINE_FORMAT.format(
            '', 0,
            account_length=self._length,
            currency_length=self.CURRENCY_LENGTH
        )
        return len(line)

    def _get_length(self):
        result = self.ACCOUNT_LENGTH
        for account in self._accounts:
            result = max(result, len(account.name))

        return result

    def _get_total(self, total):
        return self.LINE_FORMAT.format(
            'Total',
            total,
            account_length=self._length,
            currency_length=self.CURRENCY_LENGTH
        )

    def print(self):
        super().print()

        if not self._accounts:
            return 'No Accounts.'

        result = self._get_separator()
        result += self._get_title('ACCOUNTS')
        result += self._get_separator()

        total = 0
        for account in self._accounts:
            result += self._print_account(account, self._length) + '\n'
            total += account.balance

        result += self._get_separator()
        result += self._get_total(total) + '\n'
        result += self._get_separator()
        return result
