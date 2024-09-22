from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_pk>\w+)/$", consumers.ChatConsumer.as_asgi()), # as_asgi 를 호출하여 ASGI application을 생성한다.
]