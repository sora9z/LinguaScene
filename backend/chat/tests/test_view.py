from unittest.mock import MagicMock, patch
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from chat.models import ChatRoom


class ChatViewTests(APITestCase):
    def setUp(self):
        self.user = MagicMock(
            id=1,
            email="test@test.com",
            name="test",
            phone_number="010-1234-5678",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)  # 인증된 사용자 설정

    @patch("chat.views.chat_room_list_service")
    def test_chat_room_list_view_success(self, MockingChatRoomListService):
        mock_chat_room = {
            "id": 1,
            "title": "Test Room 1",
            "language": "en-US",
            "level": 1,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
            "last_message": "This is the last message",
        }
        MockingChatRoomListService.return_value = [mock_chat_room]

        url = reverse("chatroom-list")

        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), MockingChatRoomListService.return_value)
        MockingChatRoomListService.assert_called_once_with(self.user)

    @patch("chat.views.chat_room_list_service")
    def test_chat_room_list_view_exception(self, MockingChatRoomListService):
        MockingChatRoomListService.side_effect = Exception("Something went wrong")

        url = reverse("chatroom-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"detail": "Server error"})
        MockingChatRoomListService.assert_called_once_with(self.user)

    @patch("chat.views.chat_room_create_service")
    def test_chat_room_create_view_success(self, MockingChatRoomCreateService):

        data = {
            "title": "Test Room 1",
            "language": "en-US",
            "level": ChatRoom.Level.BEGINNER,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
        }

        mock_chat_room = {
            "id": 1,
            "title": "Test Room 1",
            "language": "en-US",
            "level": 1,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
        }

        MockingChatRoomCreateService.return_value = mock_chat_room

        url = reverse("chatroom-create")

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), mock_chat_room)
        data["user"] = self.user
        MockingChatRoomCreateService.assert_called_once_with(data)

    @patch("chat.views.chat_room_create_service")
    def test_chat_room_list_view_exception(self, MockingChatRoomCreateService):
        MockingChatRoomCreateService.side_effect = Exception("Something went wrong")

        url = reverse("chatroom-create")

        data = {
            "title": "",
            "language": "en-US",
            "level": ChatRoom.Level.BEGINNER,
            "situation": "Ordering food",
            "my_role": "Customer",
            "gpt_role": "Waiter",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"detail": "Server error"})
        data["user"] = self.user
        MockingChatRoomCreateService.assert_called_once_with(data)

    @patch("chat.views.chat_room_delete_service")
    def test_chat_room_delete_view_success(self, MockingChatRoomDeleteService):
        MockingChatRoomDeleteService.return_value = None  # 아무 예외 없도록 설정

        url = reverse("chatroom-delete", kwargs={"room_id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        MockingChatRoomDeleteService.assert_called_once_with(1)

    @patch("chat.views.chat_room_delete_service")
    def test_chat_room_delete_view_exception(self, MockingChatRoomDeleteService):
        MockingChatRoomDeleteService.side_effect = Exception("Unexpected error")

        url = reverse("chatroom-delete", kwargs={"room_id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"detail": "Server error"})
        MockingChatRoomDeleteService.assert_called_once_with(1)
