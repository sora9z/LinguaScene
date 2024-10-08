from django.db import models
from chat.models import ChatRoom


class Message(models.Model):
    ROLE_CHOICES = [
        ('user','User'),
        ('system','System'),
        ('assistant','Assistant'),
    ]

    chat_room = models.ForeignKey(ChatRoom,related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content}"
