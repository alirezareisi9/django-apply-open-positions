from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.core import mail
from apps.edu.models import Major, Field

from apps.accounts.views import LoginView, LogoutView

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.login_url = reverse("accounts:login")
        self.response = self.client.get(reverse("accounts:login"))

    def test_login_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_template(self):
        self.assertTemplateUsed(self.response, "registration/login.html")

    def test_login_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_login_url_resolves_loginview(self):
        view = resolve(self.login_url)
        self.assertEqual(view.func.__name__, LoginView.as_view().__name__)


class LoginLogoutLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@gmail.com"
        cls.password = "qwertyuiop12345678"

        cls.wrong_password = "asdfghjkl12345678"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.response = self.client.post(
            reverse("accounts:login"),
            {"email": self.email, "password": self.password},
            follow=True,
        )

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()

        self.response = self.client.post(
            reverse("accounts:login"),
            {"email": self.email, "password": self.password},
        )

        self.assertNotEqual(self.response.status_code, 302)
        self.assertEqual(self.response.status_code, 200)

    def test_cannot_login_by_incorrect_data(self):
        self.response = self.client.post(
            reverse("accounts:login"),
            {"email": self.email, "password": self.wrong_password},
        )

        self.assertNotEqual(self.response.status_code, 302)
        self.assertEqual(self.response.status_code, 200)

    def test_login_redirect_to_success_page(self):
        self.assertRedirects(self.response, reverse("accounts:test"))

    def test_login_correctly(self):
        self.response = self.client.get(reverse("accounts:test"))

        self.assertEqual(self.response.status_code, 200)

    def test_logout_redirect_to_success_page(self):
        self.response = self.client.get(reverse("accounts:logout"), follow=True)

        self.assertRedirects(self.response, reverse("accounts:login"))

    def test_logout_correctly(self):
        self.response = self.client.get(reverse("accounts:logout"))

        self.response = self.client.get(
            reverse("accounts:test"), follow=True
        )  # Redirects to login
        self.assertRedirects(
            self.response,
            reverse("accounts:login"),
            status_code=302,
            target_status_code=200,
        )
