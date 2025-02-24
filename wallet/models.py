from django.db import models
import uuid
from accounts.models import UserAccount

class WithdrawalSourceChoices(models.TextChoices):
    ACCOUNT = 'account'
    SALES = 'sales'

class TransactionTypeChoices(models.TextChoices):
    MINT = 'mint', 'Mint'
    DEPOSIT = 'deposit', 'Deposit'
    WITHDRAWAL = 'withdrawal', 'withdrawal'

class TransactionStatusChoices(models.TextChoices):
    SUCCESS ='success', 'Success'
    PENDING = 'pending', 'Pending'
    FAILED = 'failed', 'Failed'

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    account_balance = models.DecimalField(decimal_places=6, max_digits=30, default=0)
    sales_balance = models.DecimalField(decimal_places=6, max_digits=30, default=0)
    
    def __str__(self):
        return f"Owned by {self.user.username}"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    amount = models.DecimalField(decimal_places=6, max_digits=30)
    transaction_type = models.CharField(choices=TransactionTypeChoices.choices, max_length=20, default=TransactionTypeChoices.DEPOSIT)
    narration = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=TransactionStatusChoices.choices, max_length=20, default=TransactionStatusChoices.PENDING)
    
    
    
class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, max_digits=30)
    is_admin_verified=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_hash = models.TextField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    
class Withdrawal(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, max_digits=30)
    is_admin_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wallet_address = models.TextField()
    source = models.CharField(default=WithdrawalSourceChoices.ACCOUNT, choices=WithdrawalSourceChoices.choices, max_length=20)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    