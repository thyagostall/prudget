from prudget.uiprinter.uiaccount import UIPrinter


class UITransactionPrinter(UIPrinter):
    CURRENCY_LENGTH = 10
    DATE_LENGTH = 10
    DESCRIPTION_LENGTH = 25
    ACCOUNT_LENGTH = 10

    LINE_FORMAT = '| {} | {: <{description_length}} | {} | {: >{currency_length}.2f} | {: <{account_length}} |'

    @classmethod
    def _get_line_length(cls, transaction_length):
        line = cls.LINE_FORMAT.format(
            'C',
            '',
            '9999-99-99',
            0,
            '',
            description_length=transaction_length,
            currency_length=cls.CURRENCY_LENGTH,
            account_length=cls.ACCOUNT_LENGTH,
        )
        return len(line)

    @classmethod
    def _get_length(cls, transactions):
        result = cls.DESCRIPTION_LENGTH
        for transaction in transactions:
            result = max(result, len(transaction.description))

        return result

    @classmethod
    def _get_separator(cls, transaction_length):
        return '-' * cls._get_line_length(transaction_length) + '\n'

    @classmethod
    def _get_title(cls, transaction_length):
        length = cls._get_line_length(transaction_length)
        return '|{:^{length}}|\n'.format('TRANSACTIONS', length=length - 2)

    @classmethod
    def _get_credit_or_debit(cls, transaction):
        return type(transaction).__name__[0]

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
        result += self._get_title(transaction_length)
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