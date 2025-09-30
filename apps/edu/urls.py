from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "edu"
urlpatterns = [
    path("", views.home, name="home"),
    path("admin", views.fakeadmin, name="gottem"),
    path("detail/<int:id>/", views.uni_detail, name="detail"),
    path("profile/<int:id>/", views.prof_detail, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
