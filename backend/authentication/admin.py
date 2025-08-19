from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ("email", "fullName", "is_staff", "is_active", "isOnboarded", "createdAt")
    list_filter = ("is_staff", "is_superuser", "is_active", "isOnboarded")

    # The fields that will be shown when editing a user in admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("fullName", "bio", "profilePic", "location", "friends")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "createdAt", "updatedAt")}),
    )

    # Fields to be used when creating a user in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "fullName", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("email", "fullName")
    ordering = ("-createdAt",)


# Register the custom User model and admin
admin.site.register(User, CustomUserAdmin)
