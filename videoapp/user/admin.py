from django.contrib import admin
from user.models import UserModel, Profile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = UserModel
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username','id')  # Burada username tıklanabilir yapılıyor
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('id',)}),
    )
    readonly_fields = ('id',)

admin.site.register(UserModel, CustomUserAdmin)
admin.site.register(Profile)



