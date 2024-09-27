from django.test import TestCase
from unittest.mock import patch, MagicMock
from users.services import signup_service

class UserServiceTest(TestCase):
    @patch('users.services.SignupSerializer')  # signup_service에서 사용된 SignupSerializer를 모킹
    def test_signup_user_seccess(self,MockSignupSerializer):
        # Mocking
        mock_serializer = MockSignupSerializer.return_value
        mock_serializer.is_valid.return_value = True
        mock_user = MagicMock(username="testuser")
        mock_serializer.save.return_value = mock_user

        data = {
            "email":"test@test.com",
            "password":"1234"
        }
        
        signup_service(None,data)

        mock_serializer.assert_called_once_witn(data=data)
        mock_serializer.return_value.save.assert_called_once()
  


        