from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.blog.views import (
    PostListView, PostDetailView, CategoryListView, CategoryDetailView, TagListView, TagDetailView
)
from apps.blog.models import Post, Category


class PostListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post_list_url = reverse('blog:post_list')

    def setUp(self):
        self.response = self.client.get(self.post_list_url)
    
    def test_post_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_list_template(self):
        self.assertTemplateUsed(self.response, "blog/post_list.html")

    def test_post_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_post_list_url_resolves_post_list_view(self):
        view = resolve(self.post_list_url)
        self.assertEqual(view.func.view_class, PostListView)

class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        image = SimpleUploadedFile(
            "test.jpg", b"content is here", content_type="image/jpeg"
        )
        cls.post = Post.objects.create(title='11', slug='11', image=image)
        
        cls.post_detail_url = reverse('blog:post_detail', kwargs={'slug': cls.post.slug})
    
    def setUp(self):
        self.response = self.client.get(self.post_detail_url)
    
    def test_post_detail_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_detail_template(self):
        self.assertTemplateUsed(self.response, "blog/post_detail.html")

    def test_post_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_post_detail_url_resolves_post_detail_view(self):
        view = resolve(self.post_detail_url)
        self.assertEqual(view.func.view_class, PostDetailView)
    
class CategoryListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_list_url = reverse('blog:category_list')

    def setUp(self):
        self.response = self.client.get(self.category_list_url)

    def test_category_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_category_list_template(self):
        self.assertTemplateUsed(self.response, "blog/category_list.html")

    def test_category_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_category_list_url_resolves_category_list_view(self):
        view = resolve(self.category_list_url)
        self.assertEqual(view.func.view_class, CategoryListView)

class CategoryDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        image = SimpleUploadedFile(
            "test.jpg", b"content is here", content_type="image/jpeg"
        )
        cls.category = Category.objects.create(title='11', slug='11', image=image)
        
        cls.category_detail_url = reverse('blog:category_detail', kwargs={'slug': cls.category.slug})
    
    def setUp(self):
        self.response = self.client.get(self.category_detail_url)
    
    def test_category_detail_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_category_detail_template(self):
        self.assertTemplateUsed(self.response, "blog/category_detail.html")

    def test_category_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_category_detail_url_resolves_category_detail_view(self):
        view = resolve(self.category_detail_url)
        self.assertEqual(view.func.view_class, CategoryDetailView)

class TagListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag_list_url = reverse('blog:tag_list')

    def setUp(self):
        self.response = self.client.get(self.tag_list_url)
    
    def test_tag_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tag_list_template(self):
        self.assertTemplateUsed(self.response, "blog/tag_list.html")

    def test_tag_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_tag_list_url_resolves_tag_list_view(self):
        view = resolve(self.tag_list_url)
        self.assertEqual(view.func.view_class, TagListView)

class TagDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        image = SimpleUploadedFile(
            "test.jpg", b"content is here", content_type="image/jpeg"
        )
        cls.post = Post.objects.create(title='11', slug='11', image=image)
        cls.post.tags.add('11')
        
        cls.tag_detail_url = reverse('blog:tag_detail', kwargs={'slug': '11'})
    
    def setUp(self):
        self.response = self.client.get(self.tag_detail_url)
    
    def test_tag_detail_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tag_detail_template(self):
        self.assertTemplateUsed(self.response, "blog/tag_detail.html")

    def test_tag_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_tag_detail_url_resolves_tag_detail_view(self):
        view = resolve(self.tag_detail_url)
        self.assertEqual(view.func.view_class, TagDetailView)