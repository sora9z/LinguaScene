from asyncio import exceptions
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from chat.models import ChatRoom
from chat.services.chat_services import chat_room_list_service

# 유효한 데이터를 주었을 때 직렬화된 데이터를 반환하는지 확인
# 예외 발생시 처리 확인
class ChatServiceTests(TestCase):

    def setUp(self):
        self.user = MagicMock(id=1, email='test@test.com', first_name='test', last_name='user', is_active=True)

    @patch('chat.services.chat_services.ChatRoom.objects.filter')
    @patch('chat.services.chat_services.ChatRoomListSerializer') # serializer mocking
    def test_chat_room_list_service_success(self,MockChatRoomListSerializer,mock_filter):
        mock_chat_room = MagicMock() # fake chet_room instance
        mock_filter.return_value = [mock_chat_room] 

        serializer_data = [
            {
                'id': 1,
                'title': 'Test Room 1',
                'language': 'en-US',
                'level': ChatRoom.Level.BEGINNER,
                'situation': 'Ordering food',
                'situation_en': 'Ordering food in a restaurant',
                'my_role': 'Customer',
                'my_role_en': 'Customer',
                'gpt_role': 'Waiter',
                'gpt_role_en': 'Waiter',
                'last_message': 'This is the last message'
            }
        ]
        mock_serializer_instance = MockChatRoomListSerializer.return_value
        mock_serializer_instance.data = serializer_data 
        
        result = chat_room_list_service(self.user)

        self.assertEqual(result,serializer_data)
        mock_filter.assert_called_once_with(user=self.user)
        MockChatRoomListSerializer.assert_called_once_with([mock_chat_room],many=True)

    
    @patch('chat.services.chat_services.ChatRoom.objects.filter')
    def test_chat_room_list_service_exception(self,mock_filter):
        
        mock_filter.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as e: 
            chat_room_list_service(self.user)

        self.assertEqual(str(e.exception),"Database error")

        


    