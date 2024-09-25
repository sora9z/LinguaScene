from rest_framework import serializers
import json
import ast

from .models import Message



class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    @classmethod
    def get_content_list(cls, messages):
        content_list = []
        for message in messages:
            try:
                # 문자열을 딕셔너리로 변환
                content_dict = ast.literal_eval(message.content)
                # JSON 문자열로 변환 후 다시 파이썬 객체로 파싱
                content_obj = json.loads(json.dumps(content_dict))
                content_list.append(content_obj)
                print(content_list)
            except (ValueError, SyntaxError, json.JSONDecodeError) as e:
                print(f"Error parsing message content: {e}")
                # 에러 발생 시 원본 문자열 추가
                content_list.append(message.content)
        return content_list