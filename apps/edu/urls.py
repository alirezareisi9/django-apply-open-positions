from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()
# router.register(prefix='Log' , viewset=views.LogViewSet , basename="Log")


app_name = 'edu'
urlpatterns = [
    path('' , views.home , name='home'),
    path('admin' , views.fakeadmin , name="gottem"),
    path("detail/<int:id>/" , views.uni_detail , name="detail"),
    path("profile/<int:id>/" , views.prof_detail , name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)