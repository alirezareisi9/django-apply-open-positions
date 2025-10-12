import django_filters
from .models import *


class PositionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    university = django_filters.CharFilter(
        field_name="university__name", lookup_expr="icontains"
    )
    professor = django_filters.CharFilter(
        field_name="professor__last_name", lookup_expr="icontains"
    )
    major = django_filters.CharFilter(
        field_name="major__title", lookup_expr="icontains"
    )
    is_open = django_filters.BooleanFilter(lookup_expr="exact")

    class Meta:
        model = Position
        fields = ["title", "description", "university", "professor", "major", "is_open"]


class UniversityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    rank = django_filters.NumberFilter(lookup_expr="exact")
    major = django_filters.CharFilter(
        field_name="majors__title", lookup_expr="icontains"
    )

    class Meta:
        model = University
        fields = ["name", "location", "rank", "majors"]


class ProfessorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    university = django_filters.CharFilter(
        field_name="university__name", lookup_expr="icontains"
    )

    class Meta:
        model = Professor
        fields = ["first_name", "last_name", "email", "university"]


class PublicationFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    author_last_name = django_filters.CharFilter(
        field_name="authors__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = Publication
        fields = ["title", "author_last_name"]


class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    major = django_filters.CharFilter(
        field_name="major__title", lookup_expr="icontains"
    )
    professors_last_name = django_filters.CharFilter(
        field_name="professors__last_name", lookup_expr="icontains"
    )
    is_accessible = django_filters.BooleanFilter()

    class Meta:
        model = Course
        fields = ["title", "major", "professors_last_name", "is_accessible"]
