from django.contrib import admin
from .models import Wallet, Deposit, Withdrawal, Transaction

admin.site.register(Wallet)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Transaction)