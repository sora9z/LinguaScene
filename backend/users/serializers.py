from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser  # CustomUser 모델을 직접 import

class UserSerializer(serializers.ModelSerializer):
    # write_only means that this field will not be serialized
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser  # CustomUser 모델을 사용
        fields = ['email', 'username', 'password', 'phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
        )
        return user
