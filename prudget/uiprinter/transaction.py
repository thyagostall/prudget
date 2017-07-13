from prudget.uiprinter.base import UIPrinter


class UITransactionPrinter(UIPrinter):
    CURRENCY_LENGTH = 10
    DATE_LENGTH = 10
    DESCRIPTION_LENGTH = 25
    ACCOUNT_LENGTH = 10

    LINE_FORMAT = '| {} | {: <{description_length}} | {} | {: >{currency_length}.2f} | {: <{account_length}} |'

    def __init__(self, transactions):
        super().__init__()
        self._transactions = transactions
        self._length = self.DESCRIPTION_LENGTH

    def _get_line_length(self):
        line = self._get_formatted_line(
            'C',
            '',
            '9999-99-99',
            0,
            self._length,
            ''
        )
        return len(line)

    def _get_length(self):
        result = self.DESCRIPTION_LENGTH
        for transaction in self._transactions:
            result = max(result, len(transaction.description))

        return result

    @classmethod
    def _get_credit_or_debit(cls, transaction):
        result = type(transaction).__name__[0]
        if result == 'C':
            return '\033[92m' + result + '\033[0m'
        else:
            return '\033[91m' + result + '\033[0m'

    def _print_transaction(self, transaction):
        return self._get_formatted_line(self._get_credit_or_debit(transaction), transaction.description,
                                        self.format_date(transaction), transaction.value,
                                        self._length,
                                        transaction.account.name[:10])

    def _get_formatted_line(self, credit_or_debit, description, date, value, transaction_length, account_first10):
        return self.LINE_FORMAT.format(
            credit_or_debit,
            description,
            date,
            value,
            account_first10,
            description_length=transaction_length,
            currency_length=self.CURRENCY_LENGTH,
            account_length=self.ACCOUNT_LENGTH,
        )

    @classmethod
    def format_date(cls, transaction):
        return transaction.date.strftime('%Y-%m-%d')

    def print(self):
        super().print()

        if not self._transactions:
            return 'No Transactions.'

        result = self._get_separator()
        result += self._get_title('TRANSACTIONS')
        result += self._get_separator()
        for transaction in self._transactions:
            result += self._print_transaction(transaction) + '\n'

        result += self._get_separator()
        return result

    def print_transaction(self, transaction):
        self._length = max(self.DESCRIPTION_LENGTH, len(transaction.description))

        result = self._get_separator()
        result += self._print_transaction(transaction) + '\n'
        result += self._get_separator()

        return result
