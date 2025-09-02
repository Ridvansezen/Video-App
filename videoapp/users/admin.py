from django.contrib import admin
from users.models import UserModel
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = UserModel

    list_display = ("username", "email", "name", "bio", "profile_picture", "birth_date", "joined_at")
    search_fields = ("username", "email", "name")
    ordering = ("username",)
    readonly_fields = ("joined_at",)

    # Düzenleme formu
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Kişisel Bilgiler", {"fields": ("name", "email", "bio", "profile_picture", "birth_date", "joined_at")}),
    )

    # Yeni kullanıcı ekleme formu
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "name", "email", "bio", "profile_picture", "birth_date"),
        }),
    )

admin.site.register(UserModel, CustomUserAdmin)