from django.contrib import admin
from .models import *

# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'created_at']
    search_fields = ['name', 'region']

class OrganizationEmailAdmin(admin.ModelAdmin):
    list_display = ['get_organization_name', 'suffix']
    search_fields = ['organization__name', 'suffix']

    def get_organization_name(self, obj):
        return obj.organization.name
    get_organization_name.short_description = 'Organization Name'

class EmailAuthenticationAdmin(admin.ModelAdmin):
    list_display = ['obj_email', 'auth_code', 'sent_at', 'verified', 'auth_type']
    search_fields = ['obj_email', 'auth_type']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_organization_name', 'signup_at']
    search_fields = ['username', 'organization__name']

    def get_organization_name(self, obj):
        return obj.organization.name
    get_organization_name.short_description = 'Organization Name'

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)  # 加密密码
        super().save_model(request, obj, form, change)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationEmail, OrganizationEmailAdmin)
admin.site.register(EmailAuthentication, EmailAuthenticationAdmin)
admin.site.register(User, UserAdmin)