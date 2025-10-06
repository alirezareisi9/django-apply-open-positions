from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    "degree",
                ]
            },
        )
    ]
    list_display = ["title", "degree"]
    list_filter = ["degree"]
    search_fields = ["title"]


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    "majors",
                ]
            },
        )
    ]
    list_display = ["title"]
    list_filter = ["majors"]
    search_fields = ["title"]
    raw_id_fields = ["majors"]


class EducationInline(admin.TabularInline):
    model = models.Education
    fields = ("major", "university", "graduation_year")
    raw_id_fields = ("major", "university")
    extra = 1


# through: Publication->Professor
class ProfessorAuthorshipInline(admin.TabularInline):
    model = models.Authorship
    fields = ("publication",)
    raw_id_fields = ["publication"]
    extra = 1


class PublicationAuthorshipInline(admin.TabularInline):
    model = models.Authorship
    fields = ("professor",)
    raw_id_fields = ["professor"]
    extra = 1


class ProfessorTeachingInline(admin.TabularInline):
    model = models.Teaching
    fields = ("course",)
    raw_id_fields = ("course",)
    extra = 1


class CourseTeachingInline(admin.TabularInline):
    model = models.Teaching
    fields = ("professor",)
    raw_id_fields = ("professor",)
    extra = 1


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "biography",
                    "photo",
                    "research_interests",
                    "fields",
                    "university",
                    "department",
                    "awards_and_honors",
                    "projects",
                ]
            },
        )
    ]
    list_display = ["first_name", "last_name", "university"]
    list_filter = ["fields", "university"]
    search_fields = ["first_name", "last_name"]
    raw_id_fields = ["fields"]

    inlines = (
        EducationInline,
        ProfessorAuthorshipInline,
        ProfessorTeachingInline,
    )


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "professor",
                    "major",
                    "university",
                    "graduation_year",
                ]
            },
        )
    ]
    list_display = ["professor", "university"]
    list_filter = ["professor", "university"]
    search_fields = ["professor", "university"]
    raw_id_fields = ["professor", "university", "major"]


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    "file",
                ]
            },
        )
    ]
    list_display = ["title"]
    list_filter = ["authors"]
    search_fields = ["authors__first_name", "authors__last_name"]

    inlines = (PublicationAuthorshipInline,)


class UniversityUniversityCourse(admin.TabularInline):
    model = models.UniversityCourse
    fields = ('course', )
    raw_id_fields = ('course', )
    extra = 1


class CourseUniversityCourse(admin.TabularInline):
    model = models.UniversityCourse
    fields = ('university', )
    raw_id_fields = ('university', )
    extra = 1


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    "major",
                    "lesson_name",
                    "period",
                    "price",
                    "is_accessible",
                ]
            },
        )
    ]
    list_display = ["title", "major", "lesson_name", "is_accessible"]
    list_filter = ["major", "professors"]
    search_fields = ["professors__first_name", "professors_last_name"]
    raw_id_fields = ["major"]

    inlines = (CourseTeachingInline, CourseUniversityCourse, )


class UniversityImageInline(admin.TabularInline):
    model = models.UniversityImage
    fields = ("image", )
    extra = 1



@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "name",
                    "logo",
                    'location',
                    'rank',
                    "majors",
                ]
            },
        )
    ]
    list_display = ["name", "rank"]
    list_filter = ["majors"]
    search_fields = ["name", "rank", 'courses__title']
    raw_id_fields = ["majors", ]

    inlines = (UniversityImageInline, UniversityUniversityCourse, )


@admin.register(models.UniversityImage)
class UniversityImage(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "image",
                    'university',
                ]
            },
        )
    ]
    list_display = ['university']
    list_filter = ['university']
    search_fields = ['university']
    raw_id_fields = ['university']


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "title",
                    'description',
                    'university',
                    'professor',
                    'major',
                    'posted_date',
                    'deadline',
                    'is_open',
                ]
            },
        )
    ]
    list_display = ['title', 'university', 'professor', 'deadline']
    list_filter = ['posted_date', 'deadline', 'is_open',]
    search_fields = ['university', 'professor', 'major']
    raw_id_fields = ['university', 'professor']
    readonly_fields = ['posted_date', ]

    def get_form(self, request, obj, change, **kwargs):
        not_accessible_msg = _("It initializes automatically")
        help_texts = {
            "posted_date": not_accessible_msg,
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request=request, obj=obj, change=change, **kwargs)