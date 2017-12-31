from django.db.models import Sum

from transactions.models import Bucket


def get_bucket_queryset(user):
    return Bucket.objects.filter(owner=user).filter(show_balance=True)


def sum_bucket_balance(bucket_queryset):
    return sum([bucket.get_bucket_balance() for bucket in bucket_queryset])


def sum_expenses_amounts(expense_queryset):
    return expense_queryset.aggregate(total=Sum('amount'))['total']


def calculate_profit_or_loss(total_income, total_buckets, total_expenses):
    return total_income - (total_buckets + total_expenses)
