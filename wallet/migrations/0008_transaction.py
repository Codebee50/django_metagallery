# Generated by Django 5.1.6 on 2025-02-23 21:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_withdrawal_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=6, max_digits=30)),
                ('transaction_type', models.CharField(choices=[('mint', 'Mint'), ('deposit', 'Deposit'), ('withdrawal', 'withdrawal')], default='deposit', max_length=20)),
                ('narration', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
