from asyncio import exceptions
import logging

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
            raise exceptions.InvalidStateError('Invalid data')
            
     except Exception as e:
        logger.error(f"[user/service] Error during signup: {e}")
        raise e

def login_service(data):
    try:
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # token 생성
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email

            return {
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),
            }
    except exceptions.InvalidStateError as e:
        logger.error(f"[user/service] Invalid state error: {e}")
        raise e
    except Exception as e:
        logger.error(f"[user/service] Unexpected error: {e}")
        raise e