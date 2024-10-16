import os

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat.jwtAuthMiddleware import JwtAuthMiddleware
from chat.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lingua_scene.settings")

# ProtocolTypeRouter: connection이 http인지 websocket인지 판단하는 라우터
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # 세션 및 쿠키 기반 인증, 사용자 정보 접근 : WebSocket 연결을 처리할 때, scope 객체를 통해 연결된 사용자의 정보를 사용할 수 있다.
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
