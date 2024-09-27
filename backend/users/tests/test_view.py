from asyncio import exceptions
from unittest.mock import MagicMock, Mock, patch
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

class UserText(APITestCase):
    # signup tests
    @patch('users.views.signup_service')
    def test_signup_success(self,MockingSignupService):
        mock_service = MockingSignupService.return_value
        mock_user = MagicMock(email="test@test.com")
        mock_service.return_value = mock_user

        url = reverse('signup')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format = 'json') # 가상 클라이언트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('users.views.signup_service')
    def test_signup_exception_invalid(self,MockingSignupService):
        mock_service = MockingSignupService
        mock_service.side_effect = exceptions.InvalidStateError("Invalid state")

        url = reverse('signup')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'],"Invalid data")

        mock_service.assert_called_once()

    @patch('users.views.signup_service')
    def test_signup_exception(self,MockingSignupService):
        mock_service = MockingSignupService
        mock_service.side_effect = Exception("Server error")

        url = reverse('signup')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['detail'],"Server error")        

    # login tests
    @patch('users.views.login_service')
    def test_login_success(self,MockingLoginService):
        MockingLoginService.return_value = {
            'refreshToken': 'fake_refresh_token',
            'accessToken': 'fake_access_token'
        }

        url = reverse('login')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format = 'json') # 가상 클라이언트
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['refreshToken'], 'fake_refresh_token')
        self.assertEqual(response.data['accessToken'], 'fake_access_token')

    @patch('users.views.login_service')
    def test_login_exception_unauthorized(self,MockingLoginService):
        mock_service = MockingLoginService
        mock_service.side_effect = exceptions.InvalidStateError("Invalid credentials")

        url = reverse('login')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],"Invalid credentials")

        mock_service.assert_called_once()

    @patch('users.views.login_service')
    def test_login_exception(self,MockingLoginService):
        mock_service = MockingLoginService
        mock_service.side_effect = Exception("Server error")

        url = reverse('login')
        data = {
            "email":"test@test.com",
            "password":"1234"
        }

        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['detail'],"Server error")        




