from django.db import models
import uuid
from accounts.models import UserAccount


class NftStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    
class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin_approved=True, is_listed=True)
    
class Nft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='uploaded_nfts')
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True, related_name='owned_nfts')
    image = models.FileField(upload_to='nft-products/')
    price = models.DecimalField(max_digits=30, decimal_places=10)
    status = models.CharField(choices=NftStatusChoices, default=NftStatusChoices.PENDING, max_length=20)
    is_listed = models.BooleanField(default=True)
    is_admin_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.TextField()
    
    objects = models.Manager()
    approved= ApprovedManager()

    class Meta:
        ordering = ['-created_at']
class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="nft_sales")
    buyer= models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="nft_buys")
    nft = models.ForeignKey(Nft, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=30, decimal_places=10)
