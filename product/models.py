from django.db import models
import uuid
from accounts.models import UserAccount


class NftStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Nft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    image = models.FileField(upload_to='nfg-images/')
    price = models.IntegerField()
    status = models.CharField(choices=NftStatusChoices, default=NftStatusChoices.PENDING, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()