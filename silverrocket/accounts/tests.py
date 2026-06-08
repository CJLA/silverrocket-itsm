from django.test import TestCase

from accounts.models import CustomUser


class CustomUserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

    def test_email_is_saved(self):
        self.assertEqual(self.user.email, "test@example.com")

    def test_email_domain_is_normalized(self):
        user = CustomUser.objects.create_user(
            email="testnormalize@EXAMPLE.COM",
            password="password123",
        )

        self.assertEqual(
            user.email,
            "testnormalize@example.com",
        )

    def test_duplicateemail_raises_error(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email="test@example.com",
                password="password123",
            )

    def test_password_is_hashed(self):
        self.assertTrue(self.user.check_password("testpass123"))

    def test_role_default_is_technician(self):
        self.assertEqual(
            self.user.role,
            CustomUser.Roles.TECHNICIAN,
        )

    def test_user_string_returns_email(self):
        self.assertEqual(
            str(self.user),
            "test@example.com",
        )

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email="testAdmin@example.com",
            password="testpass123",
        )

        self.assertEqual(user.email, "testAdmin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                password="password123",
            )

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email="testAdmin2@example.com",
                password="testpass123",
                is_staff=False,
            )

    def test_check_password_returns_false_for_invalid_password(self):
        self.assertFalse(self.user.check_password("wrongpassword"))
