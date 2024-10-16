from unittest.mock import MagicMock, patch
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from libs.error.custom_exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed


class UserText(APITestCase):
    def setUp(self):
        self.user = MagicMock(
            id=1,
            email="test@test.com",
            name="test",
            phone_number="010-1234-5678",
            is_active=True,
        )

    # signup tests
    @patch("users.views.signup_service")
    def test_signup_success(self, MockingSignupService):
        MockingSignupService.return_value = self.user

        data = {"email": "test@test.com", "password": "1234"}

        url = reverse("signup")

        response = self.client.post(url, data, format="json")  # 가상 클라이언트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        MockingSignupService.assert_called_once_with(data)

    @patch("users.views.signup_service")
    def test_signup_exception_validation(self, MockingSignupService):
        MockingSignupService.side_effect = ValidationError("Invalid data provided.")

        url = reverse("signup")
        data = {"email": "test@test.com", "password": "1234"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"],
            "An validation error occured: Invalid data provided.",
        )

        # signup_service가 한 번 호출되었는지 확인
        MockingSignupService.assert_called_once()

    @patch("users.views.signup_service")
    def test_signup_exception(self, MockingSignupService):
        mock_service = MockingSignupService
        mock_service.side_effect = Exception("Something error")

        url = reverse("signup")
        data = {"email": "test@test.com", "password": "1234"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["detail"], "An unexpected error occurred.")

    # login tests
    @patch("users.views.login_service")
    def test_login_success(self, MockingLoginService):
        MockingLoginService.return_value = {
            "refreshToken": "fake_refresh_token",
            "accessToken": "fake_access_token",
        }

        url = reverse("login")
        data = {"email": "test@test.com", "password": "1234"}

        response = self.client.post(url, data, format="json")  # 가상 클라이언트
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["refreshToken"], "fake_refresh_token")
        self.assertEqual(response.data["accessToken"], "fake_access_token")

    @patch("users.views.login_service")
    def test_login_exception_unauthorized(self, MockingLoginService):
        mock_service = MockingLoginService
        mock_service.side_effect = AuthenticationFailed("Invalid credentials")

        url = reverse("login")
        data = {"email": "test@test.com", "password": "1234"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials")

        mock_service.assert_called_once()

    @patch("users.views.login_service")
    def test_login_exception(self, MockingLoginService):
        mock_service = MockingLoginService
        mock_service.side_effect = Exception("Something error")

        url = reverse("login")
        data = {"email": "test@test.com", "password": "1234"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["detail"], "An unexpected error occurred.")
