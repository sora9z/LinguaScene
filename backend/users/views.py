from asyncio import exceptions
import logging
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from libs.error.custom_exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import login_service, signup_service


logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = signup_service(request.data)
            logger.info(f"User created successfully: {user.email}")
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            print("custom", ve.detail)
            return Response(
                {"detail": f"An validation error occured: {str(ve.detail)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"[SignupView] Unexpected error: {str(e)}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            result = login_service(request.data)
            return Response(result, status=status.HTTP_200_OK)
        except AuthenticationFailed as af:
            return Response({"detail": str(af)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"[LoginView] Unexpected error: {str(e)}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
