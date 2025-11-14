from django.contrib import admin

from .models import Hostel, Room, SSO, Student


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


# Register SSO and Student for admin management
@admin.register(SSO)
class SSOAdmin(admin.ModelAdmin):
    list_display = ("sso_id", "name", "email", "phone", "office_location", "user")
    search_fields = ("sso_id", "name", "email")
    readonly_fields = ("created_at",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "email", "phone", "user")
    search_fields = ("student_id", "name", "email")
    # Do not show plaintext password in admin list/form
    exclude = ("password",)
