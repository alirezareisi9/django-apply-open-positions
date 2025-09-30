from django.urls import path
from django.urls import re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = "blog"
urlpatterns = [
    re_path(
        r"^posts/$",
        views.PostList.as_view(template_name="blog/post_list.html"),
        name="post_list",
    ),
    re_path(
        r"^category/post/(?P<slug>[\w\d-]+)/$",
        views.PostDetail.as_view(template_name="blog/post_detail.html"),
        name="post_detail",
    ),
    re_path(
        r"^categories/$",
        views.CategoryList.as_view(template_name="blog/category_list.html"),
        name="category_list",
    ),
    re_path(
        r"^category/(?P<slug>[\w\d-]+)/$",
        views.CategoryDetail.as_view(template_name="blog/category_detail.html"),
        name="category_detail",
    ),
    re_path(
        r"^tags/$",
        views.TagList.as_view(template_name="blog/tag_list.html"),
        name="tag_list",
    ),
    re_path(
        r"^tag /(?P<slug>[\w\d-]+)/$",
        views.PostList.as_view(template_name="blog/post_list.html"),
        name="tag_post_list",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
