from django.contrib import admin

from testing.models import Post,Room,Booking

admin.site.register(Post)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name","capacity","price_per_night")
    search_fields = ("name",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user","room","start_date", "end_date", "created_at")
    list_filter = ("start_date", "room")
    search_fields = ("user__username", "room__name")
