from django.db import models

class Business(models.Model):
    email = models.EmailField()
    minting_fee = models.DecimalField(max_digits=30, decimal_places=4)
    deposit_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']