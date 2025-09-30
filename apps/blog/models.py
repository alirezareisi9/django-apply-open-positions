from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.models import Tag as TagModel
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase


class Category(models.Model):
    parent_category = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="child_categories",
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    is_sub_category = models.BooleanField(null=True, blank=True)
    image = models.ImageField(upload_to="categories")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title

    @property
    def is_sub_category(self):
        if self.parent_category:
            return True
        return False

    def get_absolute_url(self):
        return reverse("blog:category_detail", kwargs={"slug": self.slug})


class Post(models.Model):
    categories = models.ManyToManyField("Category", related_name="posts")
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="posts")
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])
