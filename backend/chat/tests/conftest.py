import pytest
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.urls import path
from channels.routing import URLRouter, ProtocolTypeRouter

from lingua_scene.asgi import application


# pytest-django는 django_asgi_app이라는 이름의 fixture를 인식하여 ASGI 애플리케이션으로 사용
@pytest.fixture
def django_asgi_app():
    return application
