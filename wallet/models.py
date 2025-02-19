from django.db import models
import uuid
from accounts.models import UserAccount


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    account_balance = models.DecimalField(decimal_places=6, max_digits=30)
    sales_balance = models.DecimalField(decimal_places=6, max_digits=30)