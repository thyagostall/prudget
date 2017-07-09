class UIPrinter:
    ACCOUNT_LENGTH = 25
    CURRENCY_LENGTH = 10

    LINE_FORMAT = '| {: <{account_length}} | {: >{currency_length}.2f} |'

    @staticmethod
    def _print_account(account, length):
        return UIPrinter.LINE_FORMAT.format(account.name, account.balance, account_length=length, currency_length=UIPrinter.CURRENCY_LENGTH)

    @staticmethod
    def _get_line_length(account_length):
        return len(UIPrinter.LINE_FORMAT.format('', 0, account_length=account_length, currency_length=UIPrinter.CURRENCY_LENGTH))

    @staticmethod
    def _get_length(accounts):
        result = UIPrinter.ACCOUNT_LENGTH
        for account in accounts:
            result = max(result, len(account.name))

        return result

    @staticmethod
    def _get_separator(account_length):
        return '-' * UIPrinter._get_line_length(account_length) + '\n'

    def print_accounts(self, accounts):
        account_length = UIPrinter._get_length(accounts)

        result = UIPrinter._get_separator(account_length)
        for account in accounts:
            result += UIPrinter._print_account(account, account_length) + '\n'

        result += UIPrinter._get_separator(account_length)
        return result
