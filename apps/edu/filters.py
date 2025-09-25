import django_filters as filters
from .models import *


class UniFilter(filters.FilterSet):
    class Meta:
        model = University
        fields = {
            "name": ["icontains"],
            "scholarships": ["exact"],
            "price": ["lt", "gt"],
            "courses": ["exact"],
            "majors": ["exact"],
            "location": ["iexact"],
        }


class ProfFilter(filters.FilterSet):
    class Meta:
        model = Professor
        fields = {
            "last_name": ["icontains"],
            "major": ["exact"],
            "awards_and_honors": ["icontains"],
        }
