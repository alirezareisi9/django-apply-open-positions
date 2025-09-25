from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse, resolve
from django.core import mail
from apps.edu.models import Major, Field

from apps.accounts.views import UpdateProfileView

User = get_user_model()


class UpdateProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.password = "asdfghjkl12345678"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.update_profile_url = reverse("accounts:update-profile")

    def login(self, email, password):
        login = self.client.login(email=email, password=password)
        self.assertTrue(login)

    def test_update_profile_unauthenticated_not_accessible(self):
        response = self.client.get(self.update_profile_url, follow=True)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_update_profile_authenticated_accessible(self):
        self.login(self.email, self.password)
        response = self.client.get(self.update_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_update_profile_template(self):
        self.login(self.email, self.password)
        response = self.client.get(self.update_profile_url)
        self.assertTemplateUsed(response, "registration/update_profile.html")

    def test_update_profile_does_not_contain_incorrect_html(self):
        self.login(self.email, self.password)
        response = self.client.get(self.update_profile_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_register_url_resolves_registerview(self):
        view = resolve(self.update_profile_url)
        self.assertEqual(view.func.__name__, UpdateProfileView.as_view().__name__)


class UpdateProfileLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.password = "asdfghjkl12345678"

        cls.first_name = "qwertyuiop"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.update_profile_url = reverse("accounts:update-profile")

    def login(self, email, password):
        login = self.client.login(email=email, password=password)
        self.assertTrue(login)

    def test_update_profile_work_successfuly(self):
        self.login(self.email, self.password)
        response = self.client.post(
            self.update_profile_url,
            {
                "email": self.user.email,
                "first_name": self.first_name,
                "last_name": '',
                "major": '',
                "field": '',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("accounts:test"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, self.first_name)
