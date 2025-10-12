from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "edu"
urlpatterns = [
    path(
        "positions/",
        views.PositionListView.as_view(template_name="home/position_list.html"),
        name="position-list",
    ),
    path(
        "positions/<int:pk>/",
        views.PositionDetailView.as_view(template_name="home/position_detail.html"),
        name="position-detail",
    ),
    path(
        "universities/",
        views.UniversityListView.as_view(template_name="home/university_list.html"),
        name="university-list",
    ),
    path(
        "universities/<int:pk>/",
        views.UniversityDetailView.as_view(template_name="home/university_detail.html"),
        name="university-detail",
    ),
    path(
        "professors/",
        views.ProfessorListView.as_view(template_name="home/professor_list.html"),
        name="professor-list",
    ),
    path(
        "professors/<int:pk>/",
        views.ProfessorDetailView.as_view(template_name="home/professor_detail.html"),
        name="professor-detail",
    ),
    path(
        "publications/",
        views.PublicationListView.as_view(template_name="home/publication_list.html"),
        name="publication-list",
    ),
    path(
        "publications/<int:pk>/",
        views.PublicationDetailView.as_view(
            template_name="home/publication_detail.html"
        ),
        name="publication-detail",
    ),
    path(
        "courses/",
        views.CourseListView.as_view(template_name="home/course_list.html"),
        name="course-list",
    ),
    path(
        "courses/<int:pk>/",
        views.CourseDetailView.as_view(template_name="home/course_detail.html"),
        name="course-detail",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
