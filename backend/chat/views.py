import logging
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from chat.services.chat_services import chat_room_delete_service, chat_room_list_service, chat_room_create_service

logger = logging.getLogger(__name__)

class ChatRoomListAPIView(APIView):
    def get(self,request):
        try:
            result = chat_room_list_service(request.user)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            #TODO exception 세분화 하기
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ChatRoomCreateAPIView(APIView):
    def post(self,request):
        try:
            data = request.data
            data['user'] = request.user

            chat_room_create_service(data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            #TODO exception 세분화 하기
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatRoomDeleteAPIView(APIView):
    def delete(self,request,room_id):
        try:
            chat_room_delete_service(room_id)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            #TODO exception 세분화 하기
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

        