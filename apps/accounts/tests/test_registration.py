from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.core import mail
from apps.edu.models import Major, Field

from apps.accounts.views import RegisterView, RegisterVerificationView


User = get_user_model()


class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.response = self.client.get(reverse("accounts:register"))

    # Essential Test

    def test_register_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_register_template(self):
        self.assertTemplateUsed(self.response, "registration/register.html")

    def test_register_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_register_url_resolves_registerview(self):
        view = resolve(self.register_url)
        self.assertEqual(view.func.__name__, RegisterView.as_view().__name__)


class RegisterVerificationViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@gmail.com"
        cls.password = "qwertyuiop12345678"

    def setUp(self):
        self.response = self.client.post(
            reverse("accounts:register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
            follow=True,
        )

        self.user = User.objects.filter(email=self.email).first()

    # Essential Test

    def test_register_verification_url_exists_at_correct_location(self):
        self.assertRedirects(
            self.response,
            reverse("accounts:register-verification", kwargs={"uid": self.user.uid}),
            status_code=302,
            target_status_code=200,
        )

    def test_register_verification_template(self):
        self.assertTemplateUsed(
            self.response, "registration/register_verification.html"
        )

    def test_register_verification_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_register_verification_url_resolves_register_verification_view(self):
        self.assertEqual(
            self.response.resolver_match.func.__name__,
            RegisterVerificationView.as_view().__name__,
        )


class RegistrationLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@gmail.com"
        cls.password = "qwertyuiop12345678"

    def setUp(self):
        self.response = self.client.post(
            reverse("accounts:register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
            follow=True,
        )

        self.user = User.objects.filter(email=self.email).first()

    def test_register_creates_inactive_user(self):
        self.assertFalse(self.user.is_active)

    def test_register_send_verification_email(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.email, mail.outbox[0].to)

    def test_verification_redirect(self):
        response = self.client.post(
            reverse("accounts:register-verification", kwargs={"uid": self.user.uid}),
            {"verification_code": self.user.verification_code},
        )

        self.assertRedirects(response, reverse("accounts:test"))

    def test_verification_makes_user_active(self):
        self.client.post(
            reverse("accounts:register-verification", kwargs={"uid": self.user.uid}),
            {"verification_code": self.user.verification_code},
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_verified_user_logged_in(self):
        self.client.post(
            reverse("accounts:register-verification", kwargs={"uid": self.user.uid}),
            {"verification_code": self.user.verification_code},
        )

        # Now should access website pages
        response = self.client.get(reverse("accounts:test"))

        self.assertEqual(response.status_code, 200)
