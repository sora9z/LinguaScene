import logging
import re
from chat.models import ChatRoom
from chat.serializer import (
    ChatRoomCreateSerializer,
    ChatRoomDeleteSerializer,
    ChatRoomListSerializer,
)
from chat.services.translators import google_translate

logger = logging.getLogger(__name__)


def chat_room_list_service(data):
    try:
        chat_rooms = ChatRoom.objects.filter(user=data)
        print(chat_rooms)
        if chat_rooms is None:
            return []
        serializer = ChatRoomListSerializer(chat_rooms, many=True)
        return serializer.data
    except Exception as e:
        logger.error(f"[chat/service/get] error: {e}")
        raise e


def chat_room_create_service(data):
    try:
        language = data.get("language", "Unknown")
        level = data.get("level", "Unknown")
        title = data.get("title", "Unknown")
        situation = data.get("situation", "Unknown")
        my_role = data.get("my_role", "Unknown")
        gpt_role = data.get("gpt_role", "Unknown")

        if title == "Unknown":
            data["title"] = f"Language-{language} Level-{level}"
        elif _contains_korean(title):
            data["title"] = google_translate(title, "ko", "en")
        if _contains_korean(situation):
            data["situation"] = google_translate(situation, "ko", "en")
        if _contains_korean(my_role):
            data["my_role"] = google_translate(my_role, "ko", "en")
        if _contains_korean(gpt_role):
            data["gpt_role"] = google_translate(gpt_role, "ko", "en")

        serializer = ChatRoomCreateSerializer(data=data)

        if serializer.is_valid():
            chat_room = serializer.save(user=data.get("user"))
            logger.info(f"Chat room created successfully: {chat_room.id}")
            return serializer.data
    except Exception as e:
        logger.error(f"[chat/service/create] error: {e}")
        raise e


def chat_room_delete_service(room_id, request):
    try:
        chat_room = ChatRoom.objects.get(id=room_id)

        if chat_room is None:
            return

        serializer = ChatRoomDeleteSerializer(
            data={"room_id": room_id}, context={"request": request}
        )

        if serializer.is_valid():
            chat_room.delete()
            logger.info(f"Chat room deleted successfully: {chat_room.id }")
    except Exception as e:
        logger.error(f"[chat/service/create] error: {e}")
        raise e


def _contains_korean(text: str) -> bool:
    # 한글 유니코드 범위를 정규식으로 검사
    return bool(re.search("[\u3131-\u3163\uac00-\ud7a3]", text))
