from prudget.uiprinter.base import UIPrinter


class UIEnvelopePrinter(UIPrinter):
    CURRENCY_LENGTH = 10
    DESCRIPTION_LENGTH = 25

    LINE_FORMAT = '| {: <{description_length}} | {: >{currency_length}.2f} |'

    @classmethod
    def _get_length(cls, envelopes):
        result = cls.DESCRIPTION_LENGTH
        for envelope in envelopes:
            result = max(result, len(envelope.name))

        return result

    def _print_envelope(self, envelope):
        return self.LINE_FORMAT.format(
            envelope.name,
            envelope.balance,
            description_length=self.DESCRIPTION_LENGTH,
            currency_length=self.CURRENCY_LENGTH
        )

    def _get_line_length(self, widest_item_length):
        return len(self.LINE_FORMAT.format('', 0, description_length=self.DESCRIPTION_LENGTH, currency_length=self.CURRENCY_LENGTH))

    def print(self, envelopes):
        if not envelopes:
            return 'No Envelopes.'

        envelope_length = self._get_length(envelopes)

        result = self._get_separator(envelope_length)
        result += self._get_title('ENVELOPES', envelope_length)
        result += self._get_separator(envelope_length)
        for envelope in envelopes:
            result += self._print_envelope(envelope) + '\n'

        result += self._get_separator(envelope_length)
        return result