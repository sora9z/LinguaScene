from rest_framework import serializers
import json
import ast

from .models import Message


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["role", "content", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            content_dict = ast.literal_eval(representation["content"])
            representation["content"] = json.loads(json.dumps(content_dict))
        except (ValueError, SyntaxError, json.JSONDecodeError) as e:
            print(f"Error parsing message content: {e}")
            # 에러 발생 시 원본 문자열 유지
        return representation

    @classmethod
    def get_content_list(cls, messages):
        serializer = cls(messages, many=True)
        return serializer.data
