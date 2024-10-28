from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Regions, Districts, Cities, Organizations,
    OverallClasses, RoomsType, RoomsEquipment, 
    Rooms, OrganizationStatistics, UserProfile
)

@admin.register(UserProfile)
class UserProfileAdmin(SimpleHistoryAdmin):
    search_fields = ['first_name','last_name','father_name', 'passport_id', 'pinfl', 'tel_number', 'position', 'manzil']
    list_display = ['first_name','last_name','father_name', 'tel_number']



@admin.register(Regions)
class RegionsAdmin(SimpleHistoryAdmin):
    search_fields = ['name']
    list_display = ['name']
    list_per_page = 20
    ordering = ['name']


@admin.register(Districts)
class DistrictsAdmin(SimpleHistoryAdmin):
    search_fields = ['name', 'region__name']
    list_display = ['name', 'region']
    list_filter = ['region']
    list_per_page = 20
    ordering = ['name']


@admin.register(Cities)
class CitiesAdmin(SimpleHistoryAdmin):
    search_fields = ['name', 'region__name']
    list_display = ['name', 'region']
    list_filter = ['region']
    list_per_page = 20
    ordering = ['name']


@admin.register(Organizations)
class OrganizationsAdmin(SimpleHistoryAdmin):
    search_fields = ['name', 'district__name', 'city__name']
    list_display = ['name', 'education_type', 'power', 'is_inclusive', 'rating']
    list_filter = ['education_type', 'rating', 'district', 'city']
    list_per_page = 20
    ordering = ['name']
    autocomplete_fields = ['district', 'city']


@admin.register(OverallClasses)
class OverallClassesAdmin(SimpleHistoryAdmin):
    search_fields = ['name', 'organization__name']
    list_display = ['name', 'organization', 'rooms_amount']
    list_filter = ['organization']
    list_per_page = 20
    ordering = ['name']


@admin.register(RoomsType)
class RoomsTypeAdmin(SimpleHistoryAdmin):
    search_fields = ['name']
    list_display = ['name']
    list_per_page = 20
    ordering = ['name']


@admin.register(RoomsEquipment)
class RoomsEquipmentAdmin(SimpleHistoryAdmin):
    search_fields = ['name']
    list_display = ['name', 'measure_type', 'amount', 'avilable_type', 'entered_date', 'equipment_type']
    list_filter = ['measure_type', 'avilable_type', 'equipment_type']
    list_per_page = 20
    ordering = ['name']


@admin.register(Rooms)
class RoomsAdmin(SimpleHistoryAdmin):
    search_fields = ['room_category__name']
    list_display = ['room_category', 'students_amount']
    list_filter = ['room_category']
    list_per_page = 20
    ordering = ['room_category__name']
    autocomplete_fields = ['room_category', 'room_uquipment']


@admin.register(OrganizationStatistics)
class OrganizationStatisticsAdmin(SimpleHistoryAdmin):
    list_display = ['type', 'number']
    list_filter = ['type']