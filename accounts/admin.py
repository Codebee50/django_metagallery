from django.contrib import admin
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(BaseUserAdmin):
    model = UserAccount
    list_display = ('email', 'username', 'is_staff', 'is_admin','is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')
    search_fields = ('email', 'username')
    # ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'profile_photo',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',),
        }),
    )
    

admin.site.register(UserAccount, CustomUserAdmin)
