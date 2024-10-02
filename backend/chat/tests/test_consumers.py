# 연결 테스트 : 소켓연결 테스트
# 초기 메시지 전송 테스트 : 메시지가 없을 때 프롬프르가 전송 되는지 확인
# 메시지 수신 처리 : 사용자에게 메시지를 받으면 openai로 응답이 올바르게 처리 되고 반환하는지 확인
# 잘못된 메시지 타입 처리 테스트
# mocking : openaiservice, test data생성, asgi application setting

# test data생성 및 setting
from unittest.mock import AsyncMock, MagicMock,patch
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
import pytest

from chat.consumers import ChatConsumer
from chat.models import GptMessage


def mock_user(is_authenticated=True):
    user = MagicMock(email='test@test.com')
    user.is_authenticated=is_authenticated
    return user

def mock_chat_room(pk=1, messages_count=0,initial_messages=None):
    room = MagicMock()
    room.pk = pk
    room.messages.count.return_value = messages_count
    room.get_initial_mesages.return_value= initial_messages or [
        MagicMock(role='system', content='Initial prompt.'),
        MagicMock(role='assistant', content='Initial response.')
    ]
    return room

# ASGI application setting
@pytest.fixture
def application():
    return AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/chat/(?P<room_pk>\d+)/$', ChatConsumer.as_asgi()),
        ])
    )

#! TEST:Wobsocket connection & init message 전송 확인
@pytest.mark.asyncio
@patch('chat.consumers.ChatConsumer.save_message',new_callable=AsyncMock)
@patch('chat.consumers.ChatConsumer.get_room')
@patch('chat.consumers.OpenAiService')
async def test_connect_new_room(mock_openai_service, mock_get_room, mock_save_message, application):
    # mocking openaiservice
    mock_service_instance = mock_openai_service.return_value
    mock_service_instance.get_chat_response = AsyncMock(return_value=GptMessage(role='assistant', content='Hello!'))

    # mocking user, room
    user = mock_user(is_authenticated=True)
    chat_room = mock_chat_room(pk=1,messages_count=0,initial_messages=[
        GptMessage(role='system',content='Initial prompt'),
        GptMessage(role='assistant',content='Initial response.')
    ])

    # get_room, save_mesage  method mocking
    mock_get_room.return_value = chat_room
    mock_save_message.return_value = None

    # WebsocketCommunicator 는 websocket 연결을 시물레이션할 수 있음 
    communicator = WebsocketCommunicator(application, f"/ws/chat/{chat_room.pk}/") # ASGI 애플리케이션을 전달
    communicator.scope['user'] = user
    communicator.scope['url_route'] = {'kwargs': {'room_pk': chat_room.pk}}

    connected, _ = await communicator.connect()
    
    # 연결 성공 확인
    assert connected

    # Receive initial message
    response = await communicator.receive_json_from()
    assert response['type'] == 'assistant_message'
    assert response['message']["role"] == 'assistant'
    assert response['message']["content"] == 'Hello!'

    await communicator.disconnect()

#! TEST: 메시지 수신 테스트(receive)
@pytest.mark.asyncio
@patch('chat.consumers.ChatConsumer.save_message',new_callable=AsyncMock)
@patch('chat.consumers.ChatConsumer.get_room')
@patch('chat.consumers.OpenAiService')
async def test_receive_user_message(mock_openai_service, mock_get_room, mock_save_message, application):
    mock_serevice_instance = mock_openai_service.return_value
    mock_serevice_instance.get_chat_response = AsyncMock(return_value=GptMessage(role='assistant', content='Hello!'))

    chat_room = mock_chat_room(pk=1,messages_count=2,initial_messages=[
        GptMessage(role='system',content='Initial prompt'),
        GptMessage(role='assistant',content='Initial response.')
    ])
    mock_save_message.return_value = None

    
    communicator = WebsocketCommunicator(application, f"/ws/chat/{chat_room.pk}/")
    communicator.scope['user'] = mock_user
    communicator.scope['url_route'] = {'kwargs': {'room_pk': chat_room.pk}}

    connected, _ = await communicator.connect()
    assert connected

    # 사용자 메시지 전송
    user_message = {
        "type": "user-message",
        "content": {
            "message": "Hello, Assistant!"
        }
    }
    await communicator.send_json_to(user_message)    

    response = await communicator.receive_json_from()
    assert response['type'] == 'assistant_message'
    assert response['message']['role'] == 'assistant'
    assert response['message']['content'] == 'Hello!'
    

    await communicator.disconnect()