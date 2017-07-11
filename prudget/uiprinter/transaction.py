from prudget.uiprinter.base import UIPrinter


class UITransactionPrinter(UIPrinter):
    CURRENCY_LENGTH = 10
    DATE_LENGTH = 10
    DESCRIPTION_LENGTH = 25
    ACCOUNT_LENGTH = 10

    LINE_FORMAT = '| {} | {: <{description_length}} | {} | {: >{currency_length}.2f} | {: <{account_length}} |'

    def _get_line_length(self, transaction_length):
        line = self.LINE_FORMAT.format(
            'C',
            '',
            '9999-99-99',
            0,
            '',
            description_length=transaction_length,
            currency_length=self.CURRENCY_LENGTH,
            account_length=self.ACCOUNT_LENGTH,
        )
        return len(line)

    @classmethod
    def _get_length(cls, transactions):
        result = cls.DESCRIPTION_LENGTH
        for transaction in transactions:
            result = max(result, len(transaction.description))

        return result

    @classmethod
    def _get_credit_or_debit(cls, transaction):
        result = type(transaction).__name__[0]
        if result == 'C':
            return '\033[92m' + result + '\033[0m'
        else:
            return '\033[91m' + result + '\033[0m'

    @classmethod
    def _print_transaction(cls, transaction):
        return cls.LINE_FORMAT.format(
            cls._get_credit_or_debit(transaction),
            transaction.description,
            cls.format_date(transaction),
            transaction.value,
            transaction.account.name[:10],
            description_length=cls.DESCRIPTION_LENGTH,
            currency_length=cls.CURRENCY_LENGTH,
            account_length=cls.ACCOUNT_LENGTH,
        )

    @classmethod
    def format_date(cls, transaction):
        return transaction.date.strftime('%Y-%m-%d')

    def print(self, transactions):
        if not transactions:
            return 'No Transactions.'

        transaction_length = self._get_length(transactions)

        result = self._get_separator(transaction_length)
        result += self._get_title('TRANSACTIONS', transaction_length)
        result += self._get_separator(transaction_length)
        for transaction in transactions:
            result += self._print_transaction(transaction) + '\n'

        result += self._get_separator(transaction_length)
        return result

    def print_transaction(self, transaction):
        transaction_length = self._get_length([transaction])

        result = self._get_separator(transaction_length)
        result += self._print_transaction(transaction) + '\n'
        result += self._get_separator(transaction_length)

        return result