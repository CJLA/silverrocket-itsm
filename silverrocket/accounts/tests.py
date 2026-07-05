from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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

    def test_duplicate_email_raises_error(self):
        with self.assertRaises(IntegrityError):
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

    def test_str_returns_email(self):
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


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse("accounts:register")

    def test_user_can_register(self):
        response = self.client.post(
            self.url,
            {
                "email": "newuser@example.com",
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(email="newuser@example.com")

        self.assertTrue(user.check_password("newpassword123"))
        self.assertEqual(user.email, "newuser@example.com")
        self.assertNotIn("password", response.data)

    def test_duplicate_email_returns_400(self):
        CustomUser.objects.create_user(
            email="newuser@example.com",
            password="newpassword123",
        )

        response = self.client.post(
            self.url,
            {
                "email": "newuser@example.com",
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_email_is_required(self):
        response = self.client.post(
            self.url,
            {
                "email": "",
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_required(self):
        response = self.client.post(
            self.url,
            {
                "email": "newuser@example.com",
                "password": "",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_domain_is_normalized_on_registration(self):
        response = self.client.post(
            self.url,
            {
                "email": "NewUser@Example.com",
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(email="NewUser@example.com")
        self.assertEqual(user.email, "NewUser@example.com")
        self.assertTrue(user.check_password("newpassword123"))

    def test_duplicate_email_with_different_domain_case_returns_400(self):
        CustomUser.objects.create_user(
            email="newuser@example.com",
            password="newpassword123",
        )

        response = self.client.post(
            self.url,
            {
                "email": "newuser@Example.com",
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_common_password_returns_400(self):
        response = self.client.post(
            self.url,
            {
                "email": "newuser@example.com",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.url = reverse("accounts:login")
        self.password = "testpass123"
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password=self.password,
            first_name="Test",
            last_name="User",
        )

    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            self.url,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], self.user.email)
        self.assertEqual(response.data["user"]["first_name"], self.user.first_name)
        self.assertEqual(response.data["user"]["last_name"], self.user.last_name)

    def test_login_response_does_not_include_password(self):
        response = self.client.post(
            self.url,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data["user"])

    def test_user_cannot_login_with_invalid_credentials(self):
        response = self.client.post(
            self.url,
            {
                "email": self.user.email,
                "password": "wrongpassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials.")

    def test_user_cannot_login_with_nonexistent_email(self):
        response = self.client.post(
            self.url,
            {
                "email": "nonexistent@example.com",
                "password": "somepassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials.")

    def test_login_with_missing_email_returns_400(self):
        response = self.client.post(
            self.url,
            {
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_login_email_domain_is_normalized(self):
        response = self.client.post(
            self.url,
            {
                "email": "testuser@EXAMPLE.com",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.user.email)


class UserLogoutTests(APITestCase):
    def setUp(self):
        self.url = reverse("accounts:logout")
        self.password = "testpass123"
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password=self.password,
            first_name="Test",
            last_name="User",
        )

    def test_user_can_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully logged out.")

    def test_logout_without_authentication_returns_403(self):
        self.client.logout()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_is_logged_out_after_logout(self):
        self.client.login(email=self.user.email, password=self.password)

        logout_response = self.client.post(self.url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("tickets:ticket-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
