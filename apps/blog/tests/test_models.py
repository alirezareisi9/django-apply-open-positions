from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Category


User = get_user_model()


class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(title=1, slug=1, description="1")

    def setUp(self):
        self.image = SimpleUploadedFile(
            "test.jpg", b"content file here", content_type="image/jpeg"
        )
        self.html_content = "<p>Hello <strong>world</strong>!</p>"
        self.post = Post.objects.create(
            title="11", slug="11", image=self.image, content=self.html_content
        )
        self.post.tags.add("1", "11")
        self.post.categories.add(self.category)
        self.post.save()

    def test_object(self):
        self.assertIn(self.category, self.post.categories.all())
        self.assertEqual(self.post.title, "11")
        self.assertEqual(self.post.slug, "11")

        self.post.image.open()
        self.assertEqual(self.post.image.read(), b"content file here")
        self.post.image.close()

    def test_tags_are_saved_and_retrieved(self):
        tags = self.post.tags.names()
        self.assertEqual(set(tags), {"1", "11"})

    def test_rich_text(self):
        self.assertEqual(self.post.content, self.html_content)

    def test_rich_text_image(self):
        staff = User.objects.create_superuser(
            email="test@gmail.com", password="qwertyuiop12345678"
        )

        self.client.login(email=staff.email, password="qwertyuiop12345678")

        image = SimpleUploadedFile(
            "test.jpg", b"content is here", content_type="image/jpeg"
        )
        response = self.client.post(reverse("ckeditor_upload"), {"upload": image})

        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.json())  # CKEditor returns JSON with file URL
