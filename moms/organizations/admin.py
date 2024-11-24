from django.contrib import admin
from .models import Organization, CustomUser, Role

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_main']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'organization', 'role']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
