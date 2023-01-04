from django.contrib import admin

from account.models import Account, Organization, Region



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['uid_cognito', 'email', 'first_name', 'last_name', 'organization', 'datetime_created']
    search_fields = ['uid_cognito', 'email', 'organization__name']
    list_filter = ['is_active', 'is_superuser', 'is_staff', 'is_admin']
    ordering = ['-datetime_created']
    readonly_fields = ['datetime_created', 'datetime_deleted', 'datetime_updated', 'password']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name', 'datetime_created']
    search_fields = ['name']
    list_filter = []
    ordering = ['-datetime_created']
    readonly_fields = ['datetime_created', 'datetime_deleted', 'datetime_updated']



@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name']
    search_fields = ['name']
    list_filter = []
    ordering = ['-datetime_created']
    readonly_fields = ['datetime_created', 'datetime_deleted', 'datetime_updated']

