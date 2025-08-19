from django.contrib import admin
from .models import FriendRequest

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "status", "createdAt", "updatedAt")
    list_filter = ("status", "createdAt")
    search_fields = ("sender__email", "recipient__email")
    ordering = ("-createdAt",)
