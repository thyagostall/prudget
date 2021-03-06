# Generated by Django 2.0 on 2018-01-31 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_transaction_reference_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('TU', 'Transfer between users'), ('TA', 'Transfer between accounts'), ('TB', 'Transfer between buckets')], max_length=2)),
                ('destination_transaction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='destination_transaction', to='core.Transaction')),
                ('source_transaction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='source_transaction', to='core.Transaction')),
            ],
        ),
    ]
