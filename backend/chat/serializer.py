"""채팅 관련 시리얼라이저를 정의하는 모듈."""

from rest_framework import serializers
from .models import ChatRoom


class ChatRoomListSerializer(serializers.ModelSerializer):
    """채팅방 목록을 위한 시리얼라이저."""

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "language",
            "level",
            "title",
            "situation",
            "my_role",
            "gpt_role",
            "last_message",
        ]

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return last_message.content if last_message else None


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "language",
            "level",
            "title",
            "situation",
            "my_role",
            "gpt_role",
        ]
        extra_kwargs = {
            "situation": {"required": False},
            "my_role": {"required": False},
            "gpt_role": {"required": False},
        }


class ChatRoomDeleteSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()

    def validate(self, data):
        room_id = data.get("room_id")
        user = self.context["request"].user
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
            print("??", user, chat_room)
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError("Could not find chat room with that id.")

        if chat_room.user != user:
            raise serializers.ValidationError(
                "You do not have permission to delete this chat room."
            )
        return data
