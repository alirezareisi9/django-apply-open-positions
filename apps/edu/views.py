from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User

from .filters import *


# def home(request):
#     university = University.objects.all()
#     filters = UniFilter(request.GET, queryset=university)
#     context = {"university": filters.qs, "form": filters.form}
#     return render(request, "home/home.html", context)


# def fakeadmin(request):
#     return render(request, "home/fakeadmin.html")


# def uni_detail(request, id=None):
#     uni = get_object_or_404(University, id=id)
#     # print(type(uni.name))
#     # print(type(Professor.objects.filter(university__name="")))
#     filters = ProfFilter(request.GET, queryset=Professor.objects.filter(university=uni))

#     context = {"university": uni, "professors": filters.qs, "form": filters.form}
#     return render(request, "home/detail.html", context)


# def prof_detail(request, id=None):
#     professor = get_object_or_404(Professor, id=id)
#     print(professor.name)
#     context = {
#         "professor": professor,
#     }
#     return render(request, "home/profile.html", context)
