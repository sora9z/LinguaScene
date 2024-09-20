import logging
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ChatRoom
from .serializer import ChatRoomCreateSerializer, ChatRoomListSerializer

logger = logging.getLogger(__name__)

class ChatRoomListAPIView(APIView):
    def get(self,request):
        chat_rooms = ChatRoom.objects.filter(user=request.user)
        serializer = ChatRoomListSerializer(chat_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
   


class ChatRoomCreateAPIView(APIView):
    def post(self,request):
        logger.debug(f"Request data: {request.data}")
        if 'title' not in request.data or not request.data['title']:
            language = request.data.get('language', 'Unknown')
            level = request.data.get('level', 'Unknown')
            request.data['title'] = f"Language-{language} Level-{level}"
            
        serializer = ChatRoomCreateSerializer(data=request.data)

        if serializer.is_valid():
            chat_room = serializer.save(user=request.user)
            logger.info(f"Chat room created successfully: {chat_room.id}")
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
