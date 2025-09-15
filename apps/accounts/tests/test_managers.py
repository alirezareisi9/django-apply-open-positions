import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.edu.models import Major, Field


class CustomUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.major = Major.objects.create(title="0")
        cls.field = Field.objects.create(title="0", major=cls.major)

    def test_create_user(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            User.objects.create_user(password="123")
        with self.assertRaises(TypeError):
            User.objects.create_user(email="0")

        user = User.objects.create_user(
            email="0",
            password="123",
            first_name="0",
            last_name="0",
            major=self.major,
            field=self.field,
        )

        self.assertEqual(user.email, "0")
        self.assertEqual(user.check_password("123"), True)
        self.assertEqual(user.first_name, "0")
        self.assertEqual(user.last_name, "0")
        self.assertEqual(user.major, self.major)
        self.assertEqual(user.field, self.field)

        self.assertEqual(user.date_joined.date(), datetime.date.today())

        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            User.objects.create_superuser(password="123")
        with self.assertRaises(TypeError):
            User.objects.create_superuser(email="0")

        user = User.objects.create_superuser(
            email="0",
            password="123",
            first_name="0",
            last_name="0",
            major=self.major,
            field=self.field,
        )

        self.assertEqual(user.email, "0")
        self.assertTrue(user.check_password("123"))
        self.assertEqual(user.first_name, "0")
        self.assertEqual(user.last_name, "0")
        self.assertEqual(user.major, self.major)
        self.assertEqual(user.field, self.field)

        self.assertEqual(user.date_joined.date(), datetime.date.today())

        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
