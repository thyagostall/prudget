from core.forms import TransactionForm


class DebitTransactionForm(TransactionForm):
    def save(self, commit=True):
        self.instance.amount = -abs(self.instance.amount)
        return super().save(commit=commit)
