# Generated by Django 5.1.6 on 2025-02-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_withdrawal_wallet_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='source',
            field=models.CharField(choices=[('account', 'Account'), ('sales', 'Sales')], default='account', max_length=20),
        ),
    ]
