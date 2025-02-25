from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import CustomUserManager

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    profile_photo = models.ImageField(upload_to="profile-images/", null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio =models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover-images/', null=True, blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.email