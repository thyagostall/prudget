# Generated by Django 2.0 on 2018-02-04 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_transactionlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='group_id',
        ),
    ]
