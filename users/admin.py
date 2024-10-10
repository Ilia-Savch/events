from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from users.models.users import User


@admin.register(User)
class UsersAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "ava",
                    "phone_number",
                    "email",
                    "about",
                    "is_organizer",
                ),
            },
        ),
        (
            _("Permission"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Imporant dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "about",
                    "is_organizer",
                    "ava",
                ),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "ava_display",
        "phone_number",
        "email",
        "about",
        "is_organizer",
    )
    list_display_links = ("id", "username")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "is_organizer",
    )
    search_fields = (
        "username",
        "full_name",
        "id",
        "email",
        "phone_number",
    )
    ordering = ("-id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("last_login",)

    def ava_display(self, obj):
        return obj.ava.url if obj.ava else "No image"

    ava_display.short_description = "Аватарка"
