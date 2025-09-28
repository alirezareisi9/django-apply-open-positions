from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from apps.accounts.views import ChangePasswordView, ChangePasswordDoneView

User = get_user_model()


class ChangePasswordViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.password = "asdfghjkl12345678"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.change_password_url = reverse("accounts:change-password")

    def login(self, email, password):
        login = self.client.login(email=email, password=password)
        self.assertTrue(login)

    def test_change_password_unauthenticated_not_accessible(self):
        response = self.client.get(self.change_password_url, follow=True)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_change_password_authenticated_accessible(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)

    def test_change_password_template(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_url)
        self.assertTemplateUsed(response, "registration/change_password.html")

    def test_change_password_does_not_contain_incorrect_html(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_change_password_url_resolves_change_password_view(self):
        view = resolve(self.change_password_url)
        self.assertEqual(view.func.__name__, ChangePasswordView.as_view().__name__)


class ChangePasswordDoneViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.password = "asdfghjkl12345678"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.change_password_done_url = reverse("accounts:change-password-done")

    def login(self, email, password):
        login = self.client.login(email=email, password=password)
        self.assertTrue(login)

    def test_change_password_done_unauthenticated_not_accessible(self):
        response = self.client.get(self.change_password_done_url, follow=True)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_change_password_done_authenticated_accessible(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_done_url)
        self.assertEqual(response.status_code, 200)

    def test_change_password_done_template(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_done_url)
        self.assertTemplateUsed(response, "registration/change_password_done.html")

    def test_change_password_done_does_not_contain_incorrect_html(self):
        self.login(self.email, self.password)
        response = self.client.get(self.change_password_done_url)
        self.assertNotContains(response, "Hi there! I should not be on the page.")

    def test_change_password_done_url_resolves_change_password_done_view(self):
        view = resolve(self.change_password_done_url)
        self.assertEqual(view.func.__name__, ChangePasswordDoneView.as_view().__name__)


class ChangePasswordLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@email.com"
        cls.password = "asdfghjkl12345678"
        cls.new_password = "qwertyuiop12345678"
        cls.wrong_password = "zxcvbnm12345678"

    def setUp(self):
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.change_password_url = reverse("accounts:change-password")
        self.change_password_done_url = reverse("accounts:change-password-done")

    def login(self, email, password):
        login = self.client.login(email=email, password=password)
        self.assertTrue(login)

    def test_reject_incorrect_old_password(self):
        self.login(self.email, self.password)
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": self.wrong_password,
                "new_password1": self.new_password,
                "new_password2": self.new_password,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_missmatch_new_passwords(self):
        self.login(self.email, self.password)
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": self.password,
                "new_password1": self.new_password,
                "new_password2": self.wrong_password,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_change_password_work_successfuly(self):
        self.login(self.email, self.password)
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": self.password,
                "new_password1": self.new_password,
                "new_password2": self.new_password,
            },
            follow=True,
        )
        self.assertRedirects(response, self.change_password_done_url)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))
