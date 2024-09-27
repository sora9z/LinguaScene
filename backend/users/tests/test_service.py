from asyncio import exceptions
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from users.services import login_service, signup_service
from django.contrib.auth import get_user_model

User = get_user_model()

class UserServiceTests(TestCase):
    @patch('users.services.SignupSerializer') # serializer mocking
    def test_signup_servlice_success(self,MockSignuupSerializer):

        mock_serializer = MockSignuupSerializer.return_value
        mock_serializer.is_valid.return_value = True
        mock_user = MagicMock(email='testuser@example.com') # fake user instance
        mock_serializer.save.return_value = mock_user

        data = {
            "password": "password123",
            "email": "testuser@example.com"
        }

        user = signup_service(data)

        self.assertEqual(user.email,mock_user.email)

        mock_serializer.is_valid.assert_called_once()
        mock_serializer.save.assert_called_once()
    
    @patch('users.services.SignupSerializer')
    def test_signup_service_exception_invali(self,MockSignupSerializer):
        mock_serializer = MockSignupSerializer.return_value
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'nor_field_errors':['Invalid data']}

        data = {
            "password": "password123",
            "email": "testuser@example.com"
        }

        with self.assertRaises(exceptions.InvalidStateError): 
            signup_service(data)

        mock_serializer.is_valid.assert_called_once()

    
    @patch('users.services.LoginSerializer')
    @patch('users.services.RefreshToken')
    def test_login_service_success(self,MockRefreshToken,MockLoginSerializer):
        mock_serializer = MockLoginSerializer.return_value
        mock_serializer.is_valid.return_value = True
        mock_user = MagicMock(email='testuser@example.com') # fake user instance
        mock_serializer.validated_data = {'user': mock_user} 

        mock_refresh_instance = MockRefreshToken.for_user.return_value
        mock_refresh_instance.access_token = 'fake_access_token'
        mock_refresh_instance.__str__.return_value = 'fake_refresh_token'

        data = {
            "password": "password123",
            "email": "testuser@example.com"
        }

        result = login_service(data)

        mock_serializer.is_valid.assert_called_once()
        self.assertEqual(result['refreshToken'],'fake_refresh_token')

    @patch('users.services.LoginSerializer')
    @patch('users.services.logger')
    def test_login_service_exception_invalid(self,mock_logger,MockingLoginSerializer):
        mock_serializer = MockingLoginSerializer.return_value
        mock_serializer.is_valid.side_effect = ValidationError("Invalid data")
        
        data = {
            "password": "password123",
            "email": "testuser@example.com"
        }



        with self.assertRaises(ValidationError): 
            login_service(data)
        
        mock_serializer.is_valid.assert_called_once()       
        mock_logger.error.assert_called_once()