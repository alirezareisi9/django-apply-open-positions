from typing import Any
from django.contrib import admin
from . import models


@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
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

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "created_at",
    ]

    prepopulated_fields = {"slug": ("title",)}

    raw_id_fields = [
        "parent_category",
    ]

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        help_text_fields = "It initializes automatically"
        help_texts = {
            "created_at": help_text_fields,
            "updated_at": help_text_fields,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(self, obj=obj, change=change, **kwargs)


@admin.register(models.PostModel)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Title",  # Name of collection of these fields on admin panel
            {
                "fields": [
                    "title",
                    "slug",
                    "category",
                    "image",
                    "created_at",
                    "updated_at",
                ],
            },
        ),
        (
            "Content",
            {
                "fields": ["content", "tags"],
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
        "category",
    ]
    list_display_links = [
        "title",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "category",
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
        "category",
    )  # Makes a situation for us to search and check categories with details

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        help_text_fields = "It initializes automatically"
        help_texts = {
            "created_at": help_text_fields,
            "updated_at": help_text_fields,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(self, obj=obj, change=change, **kwargs)
