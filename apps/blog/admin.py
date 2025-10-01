from typing import Any
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    "slug",
                    "image",
                    "description",
                    "parent_category",
                    "is_sub_category",
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]

    list_display = [
        "title",
        "is_sub_category",
        "parent_category",
        "created_at",
    ]
    list_filter = [
        "created_at",
        "updated_at",
        "parent_category",
    ]

    search_fields = [
        "title",
        "created_at",
    ]

    prepopulated_fields = {"slug": ("title",)}

    raw_id_fields = [
        "parent_category",
    ]

    readonly_fields = ["is_sub_category", "created_at", "updated_at"]

    def get_form(self, request, obj, change, **kwargs):
        not_accessible_msg = _("It initializes automatically")
        help_texts = {
            "is_sub_category": not_accessible_msg,
            "created_at": not_accessible_msg,
            "updated_at": not_accessible_msg,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request=request, obj=obj, change=change, **kwargs)


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Title",  # Name of collection of these fields on admin panel
            {
                "fields": [
                    "title",
                    "slug",
                    "categories",
                    "image",
                ],
            },
        ),
        (
            "Content",
            {
                "fields": ["content", "tags"],
            },
        ),
        (
            "Log",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]

    list_display = [
        "title",
        "created_at",
    ]  # cannot set a value to manytomanyfield or reverse foreign key

    list_filter = [
        "created_at",
        "updated_at",
        "categories",
    ]

    list_display_links = [
        "title",
    ]

    search_fields = [
        "title",
        "categories",
        "content",
        "created_at",
    ]

    prepopulated_fields = {
        "slug": ("title",)
        # Use this dic for link slug to name to what you write in name, write in slug field too
        # Use tuple because it is faster, in tuple when you have just one item, you should use ',' after item,
        # if you don't; django think its string, not tuple
    }

    raw_id_fields = (
        "categories",
    )  # Makes a situation for us to search and check categories with details

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    def get_form(self, request, obj, change, **kwargs):
        not_accessible_msg = _("It initializes automatically")
        help_texts = {
            "created_at": not_accessible_msg,
            "updated_at": not_accessible_msg,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request=request, obj=obj, change=change, **kwargs)
