from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_username',
        'get_clubs'
    ]
    search_fields = [
        'user__username',
        'clubs__name'
    ]

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'User username'

    def get_clubs(self, obj):
        return ','.join([club.name 
                         for club in obj.clubs.all()])
    get_clubs.short_description = 'Clubs name'

    def save_model(self, request, obj, form, change):
        if not obj.clubs.exists(): # 즐겨찾기 게시판 미지정
            obj.clubs.clear()
        
        super().save_model(request, obj, form, change)

class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    search_fields = [
        'name'
    ]

class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_region_name',
        'created_at'
    ]
    search_fields = [
        'name',
        'region__name'
    ]

    def get_region_name(self, obj):
        return obj.region.name

class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_region_name',
        'created_at'
    ]
    search_fields = [
        'name',
        'region__name'
    ]
    
    def get_region_name(self, obj):
        return obj.region.name
    get_region_name.short_description = 'Region Name'

class OrganizationEmailAdmin(admin.ModelAdmin):
    list_display = [
        'get_organization_name',
        'suffix'
    ]
    search_fields = [
        'organization__name',
        'suffix'
    ]

    def get_organization_name(self, obj):
        return obj.organization.name
    get_organization_name.short_description = 'Organization Name'

class EmailAuthenticationAdmin(admin.ModelAdmin):
    list_display = [
        'obj_email',
        'auth_code',
        'sent_at',
        'verified',
        'auth_type'
    ]
    search_fields = [
        'obj_email',
        'auth_type'
    ]

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'get_organization_name',
        'signup_at'
    ]
    search_fields = [
        'username',
        'organization__name'
    ]

    def get_organization_name(self, obj):
        if obj.organization:
            return obj.organization.name
        else:
            return 'SYSTEM'
    get_organization_name.short_description = 'Organization Name'

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)  # 암호화된 PW
        super().save_model(request, obj, form, change)

admin.site.register(Region, RegionAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationEmail, OrganizationEmailAdmin)
admin.site.register(EmailAuthentication, EmailAuthenticationAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)