from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from core.models import Transaction
from core.services import account_balance_queryset, bucket_balance_queryset


@login_required
def dashboard(request):
    all_transactions = Transaction.objects.filter(owner=request.user).order_by('-date', '-id').select_related('bucket', 'account')

    buckets = list(filter(lambda bucket: bucket.current_balance != 0, bucket_balance_queryset(request)))
    accounts = list(filter(lambda account: account.current_balance != 0, account_balance_queryset(request)))

    bucket_total = reduce(lambda accumulator, bucket: bucket.current_balance + accumulator, buckets, 0)
    account_total = reduce(lambda accumulator, account: account.current_balance + accumulator, accounts, 0)

    paginator = Paginator(all_transactions, 50)

    page = request.GET.get('p', 1)
    transactions = paginator.get_page(page)

    context = {
        'transactions': transactions,
        'buckets': buckets,
        'accounts': accounts,

        'bucket_total': bucket_total,
        'account_total': account_total,

        'balances_dont_match': 'balance-attention' if bucket_total != account_total else ''
    }
    return render(request, 'core/dashboard.html', context=context)
