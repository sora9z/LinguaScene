from unittest.mock import MagicMock, patch
from django.test import TestCase

from chat.models import ChatRoom
from chat.services.chat_services import (
    chat_room_create_service,
    chat_room_delete_service,
    chat_room_list_service,
)


# 유효한 데이터를 주었을 때 직렬화된 데이터를 반환하는지 확인
# 예외 발생시 처리 확인
class ChatServiceTests(TestCase):

    def setUp(self):
        self.user = MagicMock(
            id=1,
            email="test@test.com",
            name="test",
            phone_number="010-1234-5678",
            is_active=True,
        )

    #! get_chet_room_list_test
    @patch("chat.services.chat_services.ChatRoom.objects.filter")
    @patch("chat.services.chat_services.ChatRoomListSerializer")  # serializer mocking
    def test_chat_room_list_service_success(
        self, MockChatRoomListSerializer, mock_filter
    ):
        mock_chat_room = MagicMock()  # fake chet_room instance
        mock_filter.return_value = [mock_chat_room]

        serializer_data = [
            {
                "id": 1,
                "title": "Test Room 1",
                "language": "en-US",
                "level": ChatRoom.Level.BEGINNER,
                "situation": "Ordering food",
                "situation_en": "Ordering food in a restaurant",
                "my_role": "Customer",
                "my_role_en": "Customer",
                "gpt_role": "Waiter",
                "gpt_role_en": "Waiter",
                "last_message": "This is the last message",
            }
        ]
        mock_serializer_instance = MockChatRoomListSerializer.return_value
        mock_serializer_instance.data = serializer_data

        result = chat_room_list_service(self.user)

        self.assertEqual(result, serializer_data)
        mock_filter.assert_called_once_with(user=self.user)
        MockChatRoomListSerializer.assert_called_once_with([mock_chat_room], many=True)

    @patch("chat.services.chat_services.ChatRoom.objects.filter")
    def test_chat_room_list_service_exception(self, mock_filter):

        mock_filter.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as e:
            chat_room_list_service(self.user)

        self.assertEqual(str(e.exception), "Database error")

    #! create_chet_room_test
    @patch("chat.services.chat_services.ChatRoomCreateSerializer")
    def test_chat_room_create_service_success(self, MockingChatRoomCreateSerializer):
        mock_serializer_instance = MockingChatRoomCreateSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_chat_room = MagicMock(id=1)
        mock_serializer_instance.save.return_value = mock_chat_room

        data = {
            "title": "",
            "language": "en-US",
            "level": ChatRoom.Level.BEGINNER,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
            "user": self.user,
        }
        chat_room_create_service(data)

        self.assertEqual(
            data["title"], f"Language-{data['language']} Level-{data['level']}"
        )
        MockingChatRoomCreateSerializer.assert_called_once_with(data=data)
        mock_serializer_instance.is_valid.assert_called_once()
        mock_serializer_instance.save.assert_called_once_with(user=data["user"])

    @patch("chat.services.chat_services.ChatRoomCreateSerializer")
    def test_chat_room_create_service_exception(self, MockingChatRoomCreateSerializer):
        mock_serializer_instance = MockingChatRoomCreateSerializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Invalid data")

        data = {
            "title": "",
            "language": "en-US",
            "level": ChatRoom.Level.BEGINNER,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
            "user": self.user,
        }

        with self.assertRaises(Exception) as e:
            chat_room_create_service(data)

        self.assertEqual(str(e.exception), "Invalid data")

    #! delete_chet_room_test
    @patch("chat.services.chat_services.ChatRoom.objects.get")
    @patch("chat.services.chat_services.ChatRoomDeleteSerializer")
    def test_chat_room_delete_service_success(
        self, MockingChatRoomDeleteSerializer, mock_get
    ):
        mock_serializer_instance = MockingChatRoomDeleteSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True

        mock_chat_room = MagicMock(id=1)
        mock_get.return_value = mock_chat_room

        chat_room_delete_service(data=1)

        MockingChatRoomDeleteSerializer.assert_called_once_with(data={"room_id": 1})
        mock_serializer_instance.is_valid.assert_called_once()
        mock_get.assert_called_once_with(id=1)

    @patch("chat.services.chat_services.ChatRoom.objects.get")
    @patch("chat.services.chat_services.ChatRoomDeleteSerializer")
    def test_chat_room_delete_service_exception(
        self, MockingChatRoomDeleteSerializer, mock_get
    ):
        mock_serializer_instance = MockingChatRoomDeleteSerializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Invalid data")

        mock_chat_room = MagicMock(id=1)
        mock_get.return_value = mock_chat_room

        with self.assertRaises(Exception) as e:
            chat_room_delete_service(data=1)

        self.assertEqual(str(e.exception), "Invalid data")
        mock_serializer_instance.is_valid.assert_called_once()
        mock_get.assert_called_once_with(id=1)
