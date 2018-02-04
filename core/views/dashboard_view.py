from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core import services
from core.models import Transaction, Bucket, Account


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(owner=request.user).order_by('-date', '-id').select_related('bucket', 'account')

    buckets = Bucket.objects.filter(owner=request.user)
    accounts = Account.objects.filter(owner=request.user)

    bucket_total = services.get_query_set_balance(buckets)
    account_total = services.get_query_set_balance(accounts)

    context = {
        'transactions': transactions,
        'buckets': buckets,
        'accounts': accounts,

        'bucket_total': bucket_total,
        'account_total': account_total,
    }
    return render(request, 'core/dashboard.html', context=context)
