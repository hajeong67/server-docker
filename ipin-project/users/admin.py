from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                    "country"
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
    )