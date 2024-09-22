
# middleware.py
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from users.models import CustomUser

@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(email=payload['email'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, CustomUser.DoesNotExist):
        return AnonymousUser()

class JwtAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        auth_header = headers.get(b'authorization', None)
        
        if auth_header is not None:
            # Bearer 토큰이기 때문에 'Bearer ' 부분을 제거
            token_name, token = auth_header.decode().split()
            if token_name.lower() == 'bearer':
                scope['user'] = await get_user_from_token(token)
            else:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)