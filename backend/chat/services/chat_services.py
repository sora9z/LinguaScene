from chat.models import ChatRoom
from chat.serializer import ChatRoomListSerializer


def chat_room_list_service(data):
    try:
        chat_rooms = ChatRoom.objects.filter(user=data)
        serializer = ChatRoomListSerializer(chat_rooms, many=True)
        return serializer.data
    except Exception as e:
        raise e