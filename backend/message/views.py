from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status

from .models import Message
from .serializer import MessageListSerializer

# Create your views here.

class MessageListAPIView(APIView):
    def get(self,request,room_id):
        try:
            messages = Message.objects.filter(chat_room_id=room_id)
            content_list = MessageListSerializer.get_content_list(messages)
            return Response(content_list, status=status.HTTP_200_OK)
        except Exception as e:
            print("error",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)