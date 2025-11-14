from django.contrib import admin

from .models import Hostel, Room


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    fields = ("number", "is_booked")


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "total_rooms")
    search_fields = ("name",)
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hostel", "number", "is_booked")
    list_filter = ("hostel", "is_booked")
    search_fields = ("hostel__name", "number")
