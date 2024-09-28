import logging
from chat.models import ChatRoom
from chat.serializer import ChatRoomCreateSerializer, ChatRoomDeleteSerializer, ChatRoomListSerializer

logger = logging.getLogger(__name__)

def chat_room_list_service(data):
    try:
        chat_rooms = ChatRoom.objects.filter(user=data)
        serializer = ChatRoomListSerializer(chat_rooms, many=True)
        return serializer.data
    except Exception as e:
        logger.error(f"[chat/service/get] error: {e}")
        raise e
    
def chat_room_create_service(data):
    try:
        language = data.get('language', 'Unknown')
        level = data.get('level', 'Unknown')
        if 'title' not in data or not data['title']:
            data['title'] = f"Language-{language} Level-{level}"

        # TODO 한글인 경우 영어로 번역해서 en 필드에 넣도록 수정
        data['situation_en'] = data['situation'];
        data['my_role_en'] = data['my_role'];
        data['gpt_role_en'] = data['gpt_role'];
            
        serializer = ChatRoomCreateSerializer(data=data)

        if serializer.is_valid():
            chat_room = serializer.save(user=data.get('user'))
            logger.info(f"Chat room created successfully: {chat_room.id}")
    except Exception as e:
        logger.error(f"[chat/service/create] error: {e}")
        raise e
    
def chat_room_delete_service(data):
    try:    
        chat_room = ChatRoom.objects.get(id = data)
        
        if chat_room is None:
            return;

        serializer = ChatRoomDeleteSerializer(data={'room_id': data})
        
        if serializer.is_valid():
            chat_room.delete()
            logger.info(f"Chat room deleted successfully: {chat_room.id }")
    except Exception as e:
        logger.error(f"[chat/service/create] error: {e}")
        raise e
