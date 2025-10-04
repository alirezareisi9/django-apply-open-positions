from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'title',
                    'degree',
                ]
            }
        )
    ]
    list_display = ['title', 'degree']
    list_filter = ['degree']
    search_fields = ['title']

@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'title',
                    'majors',
                ]
            }
        )
    ]
    list_display = ['title']
    list_filter = ['majors']
    search_fields = ['title']
    raw_id_fields = ['majors']

@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'biography',
                    'photo',
                    'research_interests',
                    'fields',
                    'department',
                    'awards_and_honors',
                    'projects',
                ]
            }
        )
    ]
    list_display = ['title']
    list_filter = ['fields', 'universities__name']
    search_fields = ['title']
    raw_id_fields = ['fields']

    