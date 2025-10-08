from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .filters import *


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


class ProfessorListView(ListView):
    model = models.Professor
    context_object_name = "professors"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()


class PublicationListView(ListView):
    model = models.Publication
    context_object_name = "publications"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()


class CourseListView(ListView):
    model = models.Course
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.all()
