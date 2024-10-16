from unittest.mock import Mock, ANY
import pytest

from chat.models import ChatRoom
from users.models import CustomUser


class TestChatRoomModel:

    def test_get_initial_messages(self):
        chatroom = ChatRoom(
            user=CustomUser(),  # 사용자 인스턴스 생성
            title="Test Chat Room",
            language=ChatRoom.Language.ENGLISH,
            level=ChatRoom.Level.BEGINNER,
            situation="Coffee Shop",
            my_role="Customer",
            gpt_role="Barista",
        )
        chatroom.chat_chain = Mock()
        expected_messages = [
            {"role": "system", "content": "System message content"},
            {"role": "assistant", "content": "Assistant message content"},
        ]
        chatroom.chat_chain.get_initial_messages.return_value = expected_messages

        # Call method
        messages = chatroom.get_initial_messages()

        assert messages == expected_messages
        expected_context = {
            "gpt_name": "RolePlayingBot",
            "language": chatroom.get_language_display(),
            "situation": chatroom.situation,
            "my_role": chatroom.my_role,
            "gpt_role": chatroom.gpt_role,
            "level_string": chatroom.get_level_string(),
            "level_word": chatroom.get_level_word(),
        }
        chatroom.chat_chain.get_initial_messages.assert_called_with(expected_context)
