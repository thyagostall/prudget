class UIAccountPrinter:
    ACCOUNT_LENGTH = 25
    CURRENCY_LENGTH = 10

    ACCOUNT_LINE_FORMAT = '| {: <{account_length}} | {: >{currency_length}.2f} |'

    @classmethod
    def _print_account(cls, account, length):
        return cls.ACCOUNT_LINE_FORMAT.format(account.name, account.balance, account_length=length, currency_length=cls.CURRENCY_LENGTH)

    @classmethod
    def _get_line_length(cls, account_length):
        return len(cls.ACCOUNT_LINE_FORMAT.format('', 0, account_length=account_length, currency_length=cls.CURRENCY_LENGTH))

    @classmethod
    def _get_length(cls, accounts):
        result = cls.ACCOUNT_LENGTH
        for account in accounts:
            result = max(result, len(account.name))

        return result

    @classmethod
    def _get_separator(cls, account_length):
        return '-' * cls._get_line_length(account_length) + '\n'

    @classmethod
    def _get_title(cls, account_length):
        length = cls._get_line_length(account_length)
        return '|{:^{length}}|\n'.format('ACCOUNTS', length=length - 2)

    def print_accounts(self, accounts):
        account_length = self._get_length(accounts)

        result = self._get_separator(account_length)
        result += self._get_title(account_length)
        result += self._get_separator(account_length)
        for account in accounts:
            result += self._print_account(account, account_length) + '\n'

        result += self._get_separator(account_length)
        return result
