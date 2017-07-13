from prudget.uiprinter.base import UIPrinter


class UIEnvelopePrinter(UIPrinter):
    CURRENCY_LENGTH = 10
    DESCRIPTION_LENGTH = 25

    LINE_FORMAT = '| {: <{description_length}} | {: >{currency_length}.2f} |'

    def __init__(self, envelopes):
        super().__init__()
        self._envelopes = envelopes

    def _get_length(self):
        result = self.DESCRIPTION_LENGTH
        for envelope in self._envelopes:
            result = max(result, len(envelope.name))

        return result

    def _print_envelope(self, envelope):
        return self._format_line(envelope.balance, envelope.name)

    def _format_line(self, balance, name):
        return self.LINE_FORMAT.format(
            name,
            balance,
            description_length=self._length,
            currency_length=self.CURRENCY_LENGTH
        )

    def _get_line_length(self):
        return len(self._format_line(0, ''))

    def print(self):
        super().print()

        if not self._envelopes:
            return 'No Envelopes.'

        result = self._get_separator()
        result += self._get_title('ENVELOPES')
        result += self._get_separator()
        for envelope in self._envelopes:
            result += self._print_envelope(envelope) + '\n'

        result += self._get_separator()
        return result
