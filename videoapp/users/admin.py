from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserModel


class CustomUserAdmin(UserAdmin):
    model = UserModel

    list_display = (
        "username",
        "name",
        "birth_date",
        "joined_at",
        "is_verified",   # eklendi
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("username", "email", "name")
    ordering = ("username",)
    readonly_fields = ["joined_at"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Kişisel Bilgiler", {
            "fields": ("name", "email", "bio", "profile_picture", "birth_date", "joined_at", "last_login"),
        }),
        ("Yetkiler", {
            "fields": ("is_active", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions"),
        }),
        ("Önemli Tarihler", {"fields": ()}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1",
                "password2",
                "name",
                "email",
                "bio",
                "profile_picture",
                "birth_date",
                "is_verified",  # eklendi
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )


admin.site.register(UserModel, CustomUserAdmin)
