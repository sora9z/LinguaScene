from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logger.debug(f"Request data: {request.data}")
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User created successfully: {user.username}")
            return Response(status=status.HTTP_201_CREATED)
        
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
     serializer = LoginSerializer(data=request.data, context={'request': request})

     if serializer.is_valid():
        print(serializer.validated_data)
        user = serializer.validated_data['user']
        
        # user 인증
        logger.debug(f"Authentication result: user={user}")
        
        if user is not None:
            # token 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),

            },status = status.HTTP_200_OK)
        
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response({'error':'Invalid credentials'},status = status.HTTP_401_UNAUTHORIZED)


