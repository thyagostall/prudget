from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from transactions.models import UserModel


class Expense(UserModel):
    WEEKLY = 'WK'
    MONTHLY = 'MO'
    BIMONTHLY = 'BI'
    ANNUALLY = 'AN'
    EXPENSE_PERIODICITY = (
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (BIMONTHLY, 'Bimonthly'),
        (ANNUALLY, 'Annually'),
    )

    WEEKDAYS = (
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )

    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated = models.BooleanField(blank=True)

    due_day = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(28)])
    due_weekday = models.IntegerField(blank=True, null=True, choices=WEEKDAYS)
    periodicity = models.CharField(max_length=2, choices=EXPENSE_PERIODICITY, default=MONTHLY)

    def __str__(self):
        return '{} ({})'.format(self.description, self.amount)
