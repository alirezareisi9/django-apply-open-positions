from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import filters


class PositionListView(ListView):
    model = models.Position
    context_object_name = "positions"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()


class PositionDetailView(DetailView):
    model = models.Position
    context_object_name = "position"


class UniversityListView(ListView):
    model = models.University
    context_object_name = "universitys"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()


class UniversityDetailView(DetailView):
    model = models.University
    context_object_name = "university"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["courses"] = self.object.courses.all()
        context["majors"] = self.object.majors.all()

        return context


class ProfessorListView(ListView):
    model = models.Professor
    context_object_name = "professors"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()


class ProfessorDetailView(DetailView):
    model = models.Professor
    context_object_name = "professor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["fields"] = self.object.fields.all()

        return context


class PublicationListView(ListView):
    model = models.Publication
    context_object_name = "publications"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["authors"] = self.object.authors.all()

        return context


class PublicationDetailView(DetailView):
    model = models.Publication
    context_object_name = "publication"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["authors"] = self.object.authors.all()

        return context


class CourseListView(ListView):
    model = models.Course
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["professors"] = self.object.professors.all()

        return context


class CourseDetailView(DetailView):
    model = models.Course
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["professors"] = self.object.professors.all()

        return context
