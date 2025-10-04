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


class EducationInline(admin.TabularInline):
    model = models.Education
    fields = ('major', 'university', 'graduation_year')
    raw_id_fields = ('major', 'university')
    extra = 1


class PublicationInline(admin.TabularInline):
    model = models.Publication
    fields = ('title', 'authors', 'graduation_year')
    raw_id_fields = ('authors', )
    extra = 1


class CourseInline(admin.TabularInline):
    model = models.Course
    fields = ('title', 'major', 'lesson_name', 'professors', 'period', 'price', 'is_accessible')
    raw_id_fields = ('major', 'professors')
    extra = 1


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
                    'university',
                    'department',
                    'awards_and_honors',
                    'projects',
                ]
            }
        )
    ]
    list_display = ['first_name', 'last_name', 'university']
    list_filter = ['fields', 'university'] 
    search_fields = ['first_name', 'last_name']
    raw_id_fields = ['fields']

    inlines = (EducationInline, )


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'professor',
                    'major',
                    'university',
                    'graduation_year',
                ]
            }
        )
    ]
    list_display = ['professor', 'university']
    list_filter = ['professor', 'university']
    search_fields = ['professor', 'university']
    raw_id_fields = ['professor', 'university', 'major']


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'title',
                    'authors',
                    'file',
                ]
            }
        )
    ]
    list_display = ['title']
    list_filter = ['authors']
    search_fields = ['authors__first_name', 'authors__last_name']
    raw_id_fields = ['authors']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Main',
            {
                'fields': [
                    'title',
                    'major',
                    'lesson_name',
                    'professors',
                    'period',
                    'price',
                    'is_accessible',
                ]
            }
        )
    ]
    list_display = ['title', 'major', 'lesson_name', 'is_accessible']
    list_filter = ['major', 'professors']
    search_fields = ['professors__first_name', 'professors_last_name']
    raw_id_fields = ['major', 'professors']