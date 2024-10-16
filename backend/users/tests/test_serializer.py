from unittest.mock import MagicMock, patch
from django.test import TestCase
from rest_framework import serializers

from users.serializers import LoginSerializer


class UserSerializerTests(TestCase):
    @patch('users.serializers.authenticate') 
    def test_login_serializer_success(self,MockingAuthenticate):
        mock_user = MagicMock(email="test@test.com")
        mock_authenticate = MockingAuthenticate
        mock_authenticate.return_value = mock_user

        data = {
            "email": "test@test.com",
            "password": "password123"
        }

        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        mock_authenticate.assert_called_once_with(
            request = None,email = data['email'],password = data['password']
        )
        self.assertEqual(validated_data['user'], mock_user)

    @patch('users.serializers.authenticate') 
    def test_login_serializer_exception(self,MockingAuthenticate):
        mock_authenticate = MockingAuthenticate
        mock_authenticate.return_value = None

        data = {
            "email": "test@test.com",
            "password": "password123"
        }

        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        



        



        
        
