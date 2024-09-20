from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser  # CustomUser 모델을 직접 import

from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    # write_only means that this field will not be serialized
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser  # CustomUser 모델을 사용
        fields = ['email','password','first_name','last_name','phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get('email')
        password = data.get('password')

        # 사용자 인증을 위한 validate 
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        return {
            'user':user,
        }