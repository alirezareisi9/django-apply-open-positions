from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import ListView, DetailView
from taggit import models as TaggitModels
from . import models


class PostListView(ListView):
    model = models.Post

    paginate_by = 12

    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = self.model.objects.all().order_by("-created_at")
        return queryset


class PostDetailView(DetailView):
    model = models.Post

    context_object_name = "post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostDetailView, self).get_context_data(**kwargs)
        related_categories = self.object.categories.all()[:5]
        similar_posts = self.object.tags.similar_objects()[:5]
        context["categories"] = related_categories
        context["similar_posts"] = similar_posts
        return context


class CategoryListView(ListView):
    model = models.Category

    paginate_by = 12

    context_object_name = "categories"

    def get_queryset(self):
        return self.model.objects.all().order_by("-created_at")


class CategoryDetailView(DetailView):
    model = models.Category

    context_object_name = "category"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        related_posts = self.object.posts.all()[:5]
        context["posts"] = related_posts
        return context


class TagListView(ListView):
    model = TaggitModels.Tag

    context_object_name = "tags"


class TagDetailView(DetailView):
    model = TaggitModels.Tag

    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tagged_posts = models.Post.objects.filter(tags=self.object)
        related_categories = models.Category.objects.filter(posts__in=tagged_posts)
        context["posts"] = tagged_posts
        context["categories"] = related_categories
        return context
