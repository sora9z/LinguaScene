import logging

from django.db import IntegrityError
from rest_framework.exceptions import  AuthenticationFailed
from libs.error.custom_exceptions import ValidationError

from .serializers import LoginSerializer, SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger(__name__)

def signup_service(data):
    try:
        serializer = SignupSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User created successfully: {user.username}")
            return user
        else:
            logger.warning(f"Validation errors during signup: {serializer.errors}")
            raise ValidationError('Invalid data provided.')
    except ValidationError as ve:
        logger.warning(f"[user/service/signup] Validation error during signup: {str(ve)}")
        raise ve 
    except Exception as e:
        logger.error(f"[user/service/signup] Unexpected error during signup: {str(e)}")
        raise e  

def login_service(data):
    try:
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # 토큰 생성
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email

            logger.info(f"User logged in successfully: {user.email}")
            return {
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),
            }
        else:
            logger.warning(f"Login failed for data: {data}")
            raise AuthenticationFailed("Invalid credentials.")
    except AuthenticationFailed as af:
        logger.warning(f"Authentication failed: {str(af)}")
        raise af
    except Exception as e:
        logger.error(f"[user/service/login] Unexpected error: {str(e)}")
        raise e