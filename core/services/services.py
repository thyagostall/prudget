from core.models import Account, Bucket


def get_query_set_balance(queryset):
    total_balance = 0
    for item in queryset:
        total_balance += item.balance()
    return total_balance


def toggle_credit_debit_and_save(transaction):
    transaction.amount = -transaction.amount
    transaction.save()


def account_balance_queryset(request):
    return Account.objects.raw(
        '''SELECT a.*, SUM(t.amount) current_balance 
           FROM core_account a JOIN core_transaction t ON t.account_id = a.id 
           WHERE t.owner_id = %s 
           GROUP BY 1, 2, 3
        ''',
        (request.user.id,))


def bucket_balance_queryset(request):
    return Bucket.objects.raw(
        '''SELECT b.*, SUM(t.amount) current_balance 
           FROM core_bucket b JOIN core_transaction t ON t.bucket_id = b.id 
           WHERE t.owner_id = %s 
           GROUP BY 1, 2, 3
        ''',
        (request.user.id,))
