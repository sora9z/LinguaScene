
from rest_framework import serializers

from .models import ChatRoom

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
    
class ChatRoomDeleteSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()

    def validate(self, data):
        room_id = data.get('room_id')
        user = self.context['request'].user
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError("Could not find chat room with that id.")
        
        if chat_room.user != user:
            raise serializers.ValidationError("You do not have permission to delete this chat room.")
        
        return data
