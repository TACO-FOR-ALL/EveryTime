from django.contrib import admin

from .models import *

class RegionBoardAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_region_name',
        'created_at'
    ]
    search_fields = [
        'region__name',
        'name'
    ]

    def get_region_name(self, obj):
        return obj.region.name
    get_region_name.short_description = 'Region Name'

class OrganizationBoardAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_region_name',
        'get_organization_name',
        'created_at'
    ]
    search_fields = [
        'organization__name',
        'region__name',
        'name'
    ]

    def get_region_name(self, obj):
        return obj.region.name
    get_region_name.short_description = 'Region Name'

    def get_organization_name(self, obj):
        return obj.organization.name
    get_organization_name.short_description = 'Organization Name'

class ClubBoardAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_region_name',
        'get_club_name',
        'created_at'
    ]
    search_fields = [
        'club__name',
        'region__name',
        'name'
    ]

    def get_region_name(self, obj):
        return obj.region.name
    get_region_name.short_description = 'Region Name'

    def get_club_name(self, obj):
        return obj.club.name
    get_club_name.short_description = 'Club Name'

admin.site.register(RegionBoard, RegionBoardAdmin)
admin.site.register(OrganizationBoard, OrganizationBoardAdmin)
admin.site.register(ClubBoard, ClubBoardAdmin)