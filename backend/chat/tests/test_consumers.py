# 연결 테스트 - connect, disconnect
# 메시지 처리 테스트 - recieve, handle_initial_message, handle_user_message
# 헬퍼 함수 테스트 - _append_to_message_buffer, send_message, send_error
# 데이터베이스 상호작용 테스트 - save_message. get_room, load_existing_message
# 얘외 추가하면서 테스트코드 같이 붙이기 

# test data생성 및 setting
from unittest.mock import AsyncMock, MagicMock,patch
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
import pytest
from asgiref.sync import sync_to_async

from chat.consumers import ChatConsumer
from chat.models import ChatRoom, GptMessage
from chat.tests.conftest import django_asgi_app


def mock_user(is_authenticated=True):
    user = MagicMock(email='test@test.com')
    user.is_authenticated=is_authenticated
    return user

def mock_chat_room(pk=1, messages_count=0,initial_messages=None):
    room = MagicMock()
    room.pk = pk
    room.messages.count.return_value = messages_count
    room.get_initial_setting.return_value='initial_setting'
    return room

#! 연결 테스트 - connct
@pytest.mark.asyncio
@patch('chat.consumers.ChatConsumer.get_room',new_callable=AsyncMock) # AsyncMock은 async def 함수의 모킹에 특화되어 있어, 비동기 함수의 반환 값을 지정하고 동작을 모방할 수 있다.
@patch('chat.consumers.ChatConsumer.handle_initial_message')
async def test_connect_success(mock_handle_initial_message,mock_get_room,django_asgi_app):
    mock_get_room.return_value = mock_chat_room()

    communicator = WebsocketCommunicator(django_asgi_app,f"/ws/chat/1/")
    connected,_ = await communicator.connect()

    assert connected
    mock_handle_initial_message.assert_called_once()

    await communicator.disconnect()

async def test_receive_success():
    #TODO
    print("tste")

async def test_handle_initial_message_success():
    # TODO
    print("tste")


#! 메시지 처리 테스트 - recieve, handle_initial_message, handle_user_message
@pytest.mark.asyncio
@patch('chat.consumers.ChatConsumer.handle_initial_message')
@patch('chat.consumers.ChatConsumer.get_room',new_callable=AsyncMock)
@patch('chat.consumers.ChatConsumer.get_response')
@patch('chat.consumers.ChatConsumer.save_messages')
async def test_handle_user_message_success(mock_save_messages,mock_get_response,mock_get_room,_,django_asgi_app):
    assistant_message_check ={'role':'assistant','content':'Mocked response'}
    mock_get_response.return_value = assistant_message_check
    mock_get_room.return_value = mock_chat_room()
    
    communicator = WebsocketCommunicator(django_asgi_app,f"/ws/chat/1/")
    connected, _ = await communicator.connect()
    assert connected

    message = {
        "type": "request_user_message",
        "message": {
            "content": "Hello"
        }
    }
    user_message_check = GptMessage(role="user",content=message["message"]["content"])

    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()

    assert response['type'] == 'response_assistant_message'
    assert response['message']['content'] == 'Mocked response'
    mock_get_response.assert_called_once_with(message_type=message["type"])
    mock_save_messages.assert_called_once_with([user_message_check,assistant_message_check])

    await communicator.disconnect()




# #! TEST:Wobsocket connection & init message 전송 확인
# @pytest.mark.asyncio
# @patch('chat.consumers.ChatConsumer.save_message',new_callable=AsyncMock)
# @patch('chat.consumers.ChatConsumer.get_room',new_callable=AsyncMock)
# @patch('chat.consumers.OpenAiService')
# async def test_connect_new_room(mock_openai_service, mock_get_room, mock_save_message, application):
#     # mocking openaiservice
#     mock_service_instance = mock_openai_service.return_value
#     response_message= {"initial_message":"initial_message","response":"response"}
#     mock_service_instance.get_initial_response = AsyncMock(return_value=response_message)

#     # mocking user, room
#     user = mock_user(is_authenticated=True)
#     chat_room = mock_chat_room(pk=1,messages_count=0,initial_messages=[
#         GptMessage(role='system',content='Initial prompt'),
#         GptMessage(role='assistant',content='Initial response.')
#     ])

#     # get_room, save_mesage  method mocking
#     mock_get_room.return_value = chat_room
#     mock_save_message.return_value = None

#     # WebsocketCommunicator 는 websocket 연결을 시물레이션할 수 있음 
#     communicator = WebsocketCommunicator(application, f"/ws/chat/{chat_room.pk}/") # ASGI 애플리케이션을 전달
#     communicator.scope['user'] = user
#     communicator.scope['url_route'] = {'kwargs': {'room_pk': chat_room.pk}}

#     connected, _ = await communicator.connect()
    
#     # 연결 성공 확인
#     assert connected

#     # Receive initial message
#     response = await communicator.receive_json_from()
#     assert response['type'] == 'assistant_message'
#     assert response['message']["role"] == 'assistant'
#     assert response['message']["content"] == 'Hello!'

#     await communicator.disconnect()

#! TEST: 메시지 수신 테스트(receive)
# @pytest.mark.asyncio
# @patch('chat.consumers.ChatConsumer.save_message',new_callable=AsyncMock)
# @patch('chat.consumers.ChatConsumer.get_room',new_callable=AsyncMock)
# @patch('chat.consumers.OpenAiService')
# async def test_receive_user_message(mock_openai_service, mock_get_room, mock_save_message, application):
#     mock_serevice_instance = mock_openai_service.return_value
#     mock_serevice_instance.get_chat_response = AsyncMock(return_value=GptMessage(role='assistant', content='Hello!'))

#     chat_room = mock_chat_room(pk=1,messages_count=2,initial_messages=[
#         GptMessage(role='system',content='Initial prompt'),
#         GptMessage(role='assistant',content='Initial response.')
#     ])

#     mock_get_room.return_value = chat_room 
#     mock_save_message.return_value = None

#     communicator = WebsocketCommunicator(application, f"/ws/chat/{chat_room.pk}/")
#     communicator.scope['user'] = mock_user(is_authenticated=True)
#     communicator.scope['url_route'] = {'kwargs': {'room_pk': chat_room.pk}}

#     connected, _ = await communicator.connect()
#     assert connected

#     # 사용자 메시지 전송
#     user_message = {
#         "type": "user-message",
#         "content": {
#             "message": "Hello, Assistant!"
#         }
#     }
#     await communicator.send_json_to(user_message)    

#     response = await communicator.receive_json_from()
#     assert response['type'] == 'assistant_message'
#     assert response['message']['role'] == 'assistant'
#     assert response['message']['content'] == 'Hello!'
    

#     await communicator.disconnect()