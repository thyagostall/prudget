def get_query_set_balance(queryset):
    total_balance = 0
    for item in queryset:
        total_balance += item.balance()
    return total_balance


def toggle_credit_debit_and_save(transaction):
    transaction.amount = -transaction.amount
    transaction.save()
