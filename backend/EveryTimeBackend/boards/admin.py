from django.contrib import admin

from .models import *

class UserBoardProfileAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_username',
        'get_mainboard_name',
        'get_favorite_boards'
    ]
    search_fields = [
        'user__username'
    ]

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'User username'

    def get_mainboard_name(self, obj):
        if obj.main_board:
            return obj.main_board.name
        return ''
    get_mainboard_name.short_description = 'Mainboard name'

    def get_favorite_boards(self, obj):
        return ','.join([board.name 
                         for board in obj.favorite_boards.all()])
    get_favorite_boards.short_description = 'Favorite boards name'

    def save_model(self, request, obj, form, change):
        if obj.main_board is None: # 메인 게시판 미지정
            obj.main_board = None
        if not obj.favorite_boards.exists(): # 즐겨찾기 게시판 미지정
            obj.favorite_boards.clear()
        
        super().save_model(request, obj, form, change)

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
admin.site.register(UserBoardProfile, UserBoardProfileAdmin)