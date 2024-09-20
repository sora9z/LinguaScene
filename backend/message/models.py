from django.db import models
from chat.models import ChatRoom

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom,related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
