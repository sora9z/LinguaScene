from asyncio import exceptions
import logging
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .services import login_service, signup_service

from .serializers import LoginSerializer, SignupSerializer

logger = logging.getLogger(__name__)

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = signup_service(request.data)
            logger.info(f"User created successfully: {user.username}")
            return Response(status=status.HTTP_201_CREATED)
        except exceptions.InvalidStateError:  
            return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try: 
            result = login_service(request.data)
            logger.info("User login successfully")
            return Response(result,status = status.HTTP_200_OK)
        except exceptions.InvalidStateError:  
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


