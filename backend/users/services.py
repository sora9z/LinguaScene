from asyncio import exceptions
import logging

from .serializers import SignupSerializer


logger = logging.getLogger(__name__)

def signup_service(data):
     try: 
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
           user = serializer.save()
           logger.info(f"User created successfully: {user.username}")
        else:
            raise exceptions.InvalidStateError('Invalid data')
            
     except Exception as e:
        logger.error(f"[user/service] Error during signup: {e}")
        raise e


            