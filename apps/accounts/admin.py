from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    list_display = ("last_name", "email", "major", "field")
    list_filter = ("major", "field")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Education", {"fields": ("major", "field")}),
        ("Log", {"fields": ("date_joined",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Education", {"fields": ("major", "field")}),
        ("Log", {"fields": ("date_joined",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    search_fields = ("last_name", "email")
    ordering = ("-id",)
    readonly_fields = ("date_joined",)
    raw_id_fields = ('major', 'field',)

    def get_form(self, request, obj, change, **kwargs):
        not_accessible_msg = _("It initializes automatically")
        help_texts = {
            "date_joined": not_accessible_msg,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request=request, obj=obj, change=change, **kwargs)
