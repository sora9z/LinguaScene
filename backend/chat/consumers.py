import json
from typing import List, Union
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async 

from message.models import Message
from users.models import CustomUser
from .models import ChatRoom, GptMessage
from .services.openai_service import OpenAiService


MESSAGE_TYPE = {
    'request_user_message': 'request_user_message', # 일반 메시지
    'request_system_message': 'request_system_message', # 추가 시스템 메시지
    'request_recommend_message': 'request_recommend_message', # 추천 표현 메시지 (확장 가능성 있음 그런 경우 명칭 변경 필요)
    'response_assistant_message':'response_assistant_message'
}
class MessageType:
    REQUEST_USER_MESSAGE = MESSAGE_TYPE['request_user_message']
    REQUEST_SYSTEM_MESSAGE = MESSAGE_TYPE['request_system_message']
    REQUEST_RECOMMEND_MESSAGE = MESSAGE_TYPE['request_recommend_message']
    RESPONSE_ASSISTANT_MESSAGE=MESSAGE_TYPE['response_assistant_message']

class ChatConsumer(AsyncWebsocketConsumer):
    # 처음 연결시 초기 프롬프트를 get_message에 저장
    # 초기 프롬프트를 get_response로 전달하여 openai로 보내고 응답을 받아서 반환
    # 그 응답은 초기 프롬프트에 대한 응답이므로 get_message에 추가한 후 반환 role은 assistant

    def __init__(self,*ags,**kwargs):
          super().__init__(*ags,**kwargs)
          self.room = None
          # TODO여기서 관리하는 것이 맞을까? 전체적으로 정리 후 고민해보기
          self.user_message: List[GptMessage] = [] 
          self.system_message:List[GptMessage] = [] 

          self.recommend_message:str = ""
          self.openai_service = OpenAiService()

    async def connect(self):
            self.room = await self.get_room()
            if self.room is None:
                 await self.close();
            else:
                await self.accept()
                await self.handle_initial_message();
   
                # 추천 프롬프트를 미리 조회하여 저장
                # self.recommend_message = self.room.get_recommend_message()

    async def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        if self.room is None:
            return  # 채팅방 정보가 없으면 처리하지 않음
        
        message_type = text_data_json["type"]
        if message_type == MessageType.REQUEST_USER_MESSAGE:
            await self.handle_user_message(text_data_json)
        else:
            await self.send_error(f"Invalid type: {message_type}") 
        # elif message_type==MessageType.REQUEST_RECOMMEND_MESSAGE:
        #     await self.request_recommend_message()
        # elif message_type==MessageType.REQUEST_SYSTEM_MESSAGE:
        #     await self.recommend_message()

    
    async def disconnect(self, close_code):
            pass
    
    async def handle_initial_message(self):
        if await self.get_message_count(self.room) == 0:
            
            initial_setting = self.room.get_initial_setting()
            response_message = await self.openai_service.get_initial_response(initial_setting)
            initial_system_message, response = response_message['initial_message'], response_message['response']

            await self.send_message(response)

            await self.save_messages([initial_system_message,response])
            self._append_to_message_buffer(type=MessageType.REQUEST_SYSTEM_MESSAGE,message=initial_system_message)
            self._append_to_message_buffer(type=MessageType.RESPONSE_ASSISTANT_MESSAGE,message=response)
        else :
             await self.load_existing_messages()
              
    async def handle_user_message(self,text_data_json):
        content = text_data_json["message"]['content']
        message_type = text_data_json["type"]
        user_message = GptMessage(role="user",content=content)
        self._append_to_message_buffer(type=message_type,message=user_message)

        # user가 보낸 메시지를 받아서 assistant 메시지를 반환
        assistant_message:GptMessage = await self.get_response(message_type=message_type) # GPTMessage
        await self.send_message(message=assistant_message)

        # 저장 밎 message_history update
        await self.save_messages([user_message,assistant_message])
        self._append_to_message_buffer(type="assistant_message",message=assistant_message)
  
    # TODO recommended message 추가     
    # async def handle_recommended_message(self):
    #     recommended_message = await self.get_response(command_query=self.recommend_message)

    #     await self.send(text_data=json.dumps({
    #         "type":"recommended-message",
    #         "message": recommended_message
    #         })
    #     )

    async def send_message(self,message:GptMessage):
         await self.send(
              text_data=json.dumps({
                    "type":MessageType.RESPONSE_ASSISTANT_MESSAGE,
                    "message": {
                         "role":message['role'],
                         "content":message['content']
                    }
                })
            )   
         
    async def send_error(self, error_message):
        await self.send(
            text_data=json.dumps({
                "type": "error",
                "message": error_message
            })
        )      

    @database_sync_to_async
    def get_room(self) -> ChatRoom | None:
        user:CustomUser =  self.scope['user']
        room_pk = self.scope['url_route']['kwargs']['room_pk']

        if user.is_authenticated:
            try:
                 return ChatRoom.objects.get(pk=room_pk)
            except ChatRoom.DoesNotExist:
                  return None
        return None
                
    
    async def get_response(self, message_type:str)->GptMessage:
        # 예외처리 추가
        try:
            if message_type == MessageType.REQUEST_USER_MESSAGE:
                return await self.openai_service.get_chat_response(self.user_message)
            elif message_type == MessageType.REQUEST_SYSTEM_MESSAGE:
                return await self.openai_service.get_chat_response(self.system_message)
            else : 
                raise Exception("[consumer/get_response] Invelid message type") # log로 남기기 예외는 필요할까?
        except Exception as e:
            print(f"예외 발생: {e}")
            raise e

        
    def _append_to_message_buffer(self, type,message:GptMessage):
        if type == MessageType.REQUEST_USER_MESSAGE or type ==MessageType.RESPONSE_ASSISTANT_MESSAGE:
              self.user_message.append(message)
        elif type == MessageType.REQUEST_SYSTEM_MESSAGE:
             self.system_message.append(message)
        else :
             None
        
    @database_sync_to_async
    def get_message_count(self, room):
        return room.messages.count()        
    
    @database_sync_to_async
    def save_message(self,message:GptMessage):
        msg= Message.objects.create(chat_room=self.room,role=message['role'],content=message['content'])
        msg.save()

    async def save_messages(self,messages:list[GptMessage]):
         for message in messages:
              await self.save_message(message)
    
    @database_sync_to_async
    def load_existing_messages(self):
        # Message 에서 현재 chat_room 기준으로 생성기준으로 정렬하여 가져온다
        # message.role로 구분하여 user,system,assistant 로 message를 분류한다
        messages = Message.objects.filter(chat_room=self.room).order_by('created_at')
        self.user_message.clear()  # 기존 메시지 리스트 초기화
        self.system_message.clear()  # 기존 메시지 리스트 초기화
        for message in messages:
             gpt_message = GptMessage(role=message.role,content=message.content)
             if message.role in ['user','assistant']:
                  self.user_message.append(gpt_message)
             elif message.role =='system':
                  self.system_message.append(gpt_message)
