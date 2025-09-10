from django.contrib import admin
from .models import *


admin.site.register(Professor)
# class CoursesAdmin(admin.ModelAdmin):
#     model = Courses
#     class Meta:
#         verbose_name_plural = "Courses"
# class UniversityAdmin():
#     model = University
    # class Meta:
    #     verbose_name_plural = "universities"
admin.site.register(Courses)
admin.site.register(Major)
admin.site.register(Field)

admin.site.register(University)

