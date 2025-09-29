from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.core import mail

from apps.accounts.views import (
    ResetPasswordView,
    ResetPasswordSentView,
    ResetPasswordCompleteView,
    ResetPasswordConfirmView,
)

import uuid

User = get_user_model()


class ResetPasswordViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reset_password_url = reverse("accounts:reset-password")

    def test_reset_password_accessible(self):
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_template(self):
        response = self.client.get(self.reset_password_url)
        self.assertTemplateUsed(response, "registration/reset_password.html")

    def test_reset_password_does_not_contain_incorrect_html(self):
        response = self.client.get(self.reset_password_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_reset_password_url_resolves_reset_password_view(self):
        view = resolve(self.reset_password_url)
        self.assertEqual(view.func.view_class, ResetPasswordView)


class ResetPasswordSentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reset_password_sent_url = reverse("accounts:reset-password-sent")

    def test_reset_password_sent_accessible(self):
        response = self.client.get(self.reset_password_sent_url)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_sent_template(self):
        response = self.client.get(self.reset_password_sent_url)
        self.assertTemplateUsed(response, "registration/reset_password_sent.html")

    def test_reset_password_sent_does_not_contain_incorrect_html(self):
        response = self.client.get(self.reset_password_sent_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_reset_password_sent_url_resolves_reset_password_sent_view(self):
        view = resolve(self.reset_password_sent_url)
        self.assertEqual(view.func.view_class, ResetPasswordSentView)


class ResetPasswordConfirmViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.uid = uuid.uuid4()

    def setUp(self):
        self.reset_password_confirm_url = reverse(
            "accounts:reset-password-confirm", kwargs={"uid": self.uid}
        )

    def test_reset_password_confirm_not_accessible_by_wrong_uuid(self):
        response = self.client.get(self.reset_password_confirm_url)
        self.assertEqual(response.status_code, 404)


class ResetPasswordCompleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reset_password_complete_url = reverse("accounts:reset-password-complete")

    def test_reset_password_complete_accessible(self):
        response = self.client.get(self.reset_password_complete_url)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_complete_template(self):
        response = self.client.get(self.reset_password_complete_url)
        self.assertTemplateUsed(response, "registration/reset_password_complete.html")

    def test_reset_password_complete_does_not_contain_incorrect_html(self):
        response = self.client.get(self.reset_password_complete_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_reset_password_complete_url_resolves_reset_password_complete_view(self):
        view = resolve(self.reset_password_complete_url)
        self.assertEqual(view.func.view_class, ResetPasswordCompleteView)


class ResetPasswordLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.wrong_email = "test2@gmail.com"
        cls.password1 = "asdfghjkl12345678"
        cls.password2 = "qwertyuiop12345678"
        cls.update_profile_url = reverse("accounts:update-profile")

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password1)
        self.user.save()

    def test_reject_wrong_email(self):
        response = self.client.post(
            reverse("accounts:reset-password"), {"email": self.wrong_email}
        )
        self.assertEqual(response.status_code, 200)

    def test_sent_email_correctly(self):
        response = self.client.post(
            reverse("accounts:reset-password"), {"email": self.email}, follow=True
        )
        self.assertRedirects(response, reverse("accounts:reset-password-sent"))

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.email, mail.outbox[0].to)

    def test_reset_password_confirm_open(self):
        response = self.client.get(
            reverse("accounts:reset-password-confirm", kwargs={"uid": self.user.uid})
        )
        self.assertEqual(response.status_code, 200)

    def test_miss_match_works(self):
        response = self.client.post(
            reverse("accounts:reset-password-confirm", kwargs={"uid": self.user.uid}),
            {"password1": self.password1, "password2": self.password2},
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_correctly(self):
        response = self.client.post(
            reverse("accounts:reset-password-confirm", kwargs={"uid": self.user.uid}),
            {"password1": self.password2, "password2": self.password2},
            follow=True,
        )
        self.assertRedirects(response, reverse("accounts:reset-password-complete"))

        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.password1))
        self.assertTrue(self.user.check_password(self.password2))

        self.assertTrue(self.user.is_active)
