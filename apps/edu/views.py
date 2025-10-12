from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from . import models
from . import filters


class PositionListView(FilterView):
    model = models.Position
    context_object_name = "positions"
    filterset_class = filters.PositionFilter
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("university", "professor", "major").order_by(
            "-posted_date"
        )
        return qs.distinct()


class PositionDetailView(DetailView):
    model = models.Position
    context_object_name = "position"


class UniversityListView(FilterView):
    model = models.University
    context_object_name = "universities"
    filterset_class = filters.UniversityFilter
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs.prefetch_related("courses", "majors").order_by("name")
        return qs.distinct()


class UniversityDetailView(DetailView):
    model = models.University
    context_object_name = "university"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["courses"] = self.object.courses.all()
        context["majors"] = self.object.majors.all()

        return context


class ProfessorListView(FilterView):
    model = models.Professor
    filterset_class = filters.ProfessorFilter
    context_object_name = "professors"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.select_related("university")
            .prefetch_related("fields")
            .order_by("university__rank")
            .distinct()
        )
        return qs


class ProfessorDetailView(DetailView):
    model = models.Professor
    context_object_name = "professor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["fields"] = self.object.fields.all()

        return context


class PublicationListView(FilterView):
    model = models.Publication
    filterset_class = filters.PublicationFilter
    context_object_name = "publications"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("authors").order_by("authors__last_name").distinct()
        return qs


class PublicationDetailView(DetailView):
    model = models.Publication
    context_object_name = "publication"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["authors"] = self.object.authors.all()

        return context


class CourseListView(FilterView):
    model = models.Course
    filterset_class = filters.CourseFilter
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.select_related("major")
            .prefetch_related("professors")
            .order_by("professors__last_name")
        )
        return qs


class CourseDetailView(DetailView):
    model = models.Course
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["professors"] = self.object.professors.all()

        return context
