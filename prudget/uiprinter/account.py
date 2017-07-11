from prudget.uiprinter.base import UIPrinter


class UIAccountPrinter(UIPrinter):
    ACCOUNT_LENGTH = 25
    CURRENCY_LENGTH = 10

    LINE_FORMAT = '| {: <{account_length}} | {: >{currency_length}.2f} |'

    @classmethod
    def _print_account(cls, account, length):
        return cls.LINE_FORMAT.format(
            account.name,
            account.balance,
            account_length=length,
            currency_length=cls.CURRENCY_LENGTH
        )

    def _get_line_length(self, account_length):
        line = self.LINE_FORMAT.format(
            '', 0,
            account_length=account_length,
            currency_length=self.CURRENCY_LENGTH
        )
        return len(line)

    @classmethod
    def _get_length(cls, accounts):
        result = cls.ACCOUNT_LENGTH
        for account in accounts:
            result = max(result, len(account.name))

        return result

    def print(self, accounts):
        if not accounts:
            return 'No Accounts.'

        account_length = self._get_length(accounts)

        result = self._get_separator(account_length)
        result += self._get_title('ACCOUNTS', account_length)
        result += self._get_separator(account_length)

        total = 0
        for account in accounts:
            result += self._print_account(account, account_length) + '\n'
            total += account.balance

        result += self._get_separator(account_length)
        result += self.LINE_FORMAT.format(
            'Total',
            total,
            account_length=account_length,
            currency_length=self.CURRENCY_LENGTH
        ) + '\n'
        result += self._get_separator(account_length)
        return result