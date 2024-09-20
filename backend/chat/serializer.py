
from .models import ChatRoom
from rest_framework import serializers


class ChatRoomListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()  

    class Meta:
        model = ChatRoom
        fields = [
            'id','language', 'level', 'title','situation', 'situation_en', 'my_role', 'my_role_en', 'gpt_role', 'gpt_role_en', 'last_message'
        ]

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return last_message.content if last_message else None

class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            'id','language', 'level', 'title','situation', 'situation_en', 'my_role', 'my_role_en', 'gpt_role', 'gpt_role_en'
        ]
        extra_kwargs = {
            'situation_en': {'required': False},
            'my_role_en': {'required': False},
            'gpt_role_en': {'required': False}
        }
    