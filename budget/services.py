import datetime

from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce

from transactions.models import Bucket


def get_bucket_queryset(user):
    return Bucket.objects.filter(owner=user).filter(show_balance=True)


def sum_total_income_for_month(user, date):
    from transactions.models import Transaction, Bucket

    try:
        income_bucket = Bucket.objects\
            .filter(owner=user)\
            .get(name='Income')
    except ObjectDoesNotExist:
        return Decimal(0)

    return Transaction.objects.filter(owner=user) \
        .annotate(real_reference_date=Coalesce('reference_date', 'date')) \
        .filter(real_reference_date__month=date.month) \
        .filter(real_reference_date__year=date.year) \
        .filter(bucket=income_bucket) \
        .aggregate(total=Sum('amount'))['total'] or Decimal(0)


def sum_bucket_values(bucket_queryset):
    return sum([bucket.get_bucket_value() for bucket in bucket_queryset])


def sum_expenses_amounts(expense_queryset):
    return expense_queryset.aggregate(total=Sum('amount'))['total']


def calculate_profit_or_loss(total_income, total_buckets, total_expenses):
    total_income = total_income or Decimal(0)
    total_buckets = total_buckets or Decimal(0)
    total_expenses = total_expenses or Decimal(0)

    return total_income - (total_buckets + total_expenses)


def was_expense_paid(expense):
    from transactions.models import Transaction

    current_date = datetime.datetime.today()
    user_expenses = Transaction.objects \
        .filter(owner=expense.owner) \
        .filter(expense=expense) \
        .annotate(real_reference_date=Coalesce('reference_date', 'date'))

    if expense.periodicity == expense.MONTHLY:
        return user_expenses \
            .filter(real_reference_date__year=current_date.year) \
            .filter(real_reference_date__month=current_date.month) \
            .exists()
    elif expense.periodicity == expense.BIMONTHLY:
        previous_month_date = previous_month_from_date(current_date)
        return user_expenses \
            .filter((
                        Q(real_reference_date__month=current_date.month) &
                        Q(real_reference_date__year=current_date.year)
                    ) | (
                        Q(real_reference_date__month=previous_month_date.month) &
                        Q(real_reference_date__year=previous_month_date.year)
                    )) \
            .exists()
    else:
        return user_expenses \
            .filter(real_reference_date__year=current_date.year) \
            .exists()


def previous_month_from_date(current_date):
    current_date = current_date.replace(day=1)
    return current_date - datetime.timedelta(days=1)
