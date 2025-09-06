from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import ListView, DetailView
from taggit import models as TaggitModels
from . import models


class PostList(ListView):
    model = models.PostModel

    paginate_by = 12

    context_object_name = 'post_list'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = models.PostModel.objects.all().order_by('-created_at')
        tag_slug = self.kwargs.get('slug')
        if tag_slug:
            tag = get_object_or_404(TaggitModels.Tag, slug=tag_slug)
            return queryset.filter(tags__in=[tag])
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostList, self).get_context_data(**kwargs)
        tag_slug = self.kwargs.get('slug')
        if tag_slug:
            tag = get_object_or_404(TaggitModels.Tag, slug=tag_slug)
            context['tag'] = tag
        return context
        


class PostDetail(DetailView):
    model = models.PostModel

    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostDetail, self).get_context_data(**kwargs)
        related_categories = self.object.category.all()[:5]
        similar_posts = self.object.tags.similar_objects()[:5]
        context['categories'] = related_categories
        context['similar_posts'] = similar_posts
        return context


class CategoryList(ListView):
    model = models.CategoryModel
    queryset = model.objects.all().order_by('-created_at')

    paginate_by = 12

    context_object_name = 'category_list'


class CategoryDetail(DetailView):
    model = models.CategoryModel

    context_object_name = 'category'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        related_posts = self.object.rel_post_category.all()[:5]
        context['posts'] = related_posts
        return context
    

class TagList(ListView):
    model = TaggitModels.Tag

    context_object_name = 'tags'