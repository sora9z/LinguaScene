import json
from typing import List
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async 

from message.models import Message
from users.models import CustomUser
from .models import ChatRoom, GptMessage
from .services.openai_service import OpenAiService

class ChatConsumer(AsyncWebsocketConsumer):
    # 처음 연결시 초기 프롬프트를 get_message에 저장
    # 초기 프롬프트를 get_query로 전달하여 openai로 보내고 응답을 받아서 반환
    # 그 응답은 초기 프롬프트에 대한 응답이므로 get_message에 추가한 후 반환 role은 assistant

    def __init__(self,*ags,**kwargs):
          super().__init__(*ags,**kwargs)
          self.room = None
          self.get_message: List[GptMessage] = []
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
        if message_type =="user-message":
             await self.handle_user_message(self,text_data_json)
        else:
            await self.send_error(f"Invalid type: {message_type}") 
        # elif message_type=="request-recommend-message":
        #     await self.recommend_message()
    
    async def disconnect(self, close_code):
            pass
    
    async def handle_initial_message(self):
         if await self.get_message_count(self.room) == 0:
            initial_messages = self.room.get_initial_messages() 
            await self.save_messages(self.room, initial_messages)
            self.get_message = initial_messages
            
            await self.send(  
                text_data=json.dumps({
                    "type": "assistant_message",
                    "message": await self.get_query()
                })
            )         
    
    async def handle_user_message(self,text_data_json):
        # user_message = HumanMessage(contnt=text_data_json["content"]["message"])
        await self.save_message(self.room, GptMessage(role="user",content=text_data_json["content"]["message"]))
        # user가 보낸 메시지를 받아서 assistant 메시지를 반환
        assistant_message = await self.get_query(user_query=text_data_json["content"]["message"])
        await self.save_message(self.room, assistant_message)
        await self.send(text_data=json.dumps({
             "type": "assistant_message",
             "message": assistant_message
             })
        )         
        self.send(text_data=json.dumps({
                "type":"error",
                "message":f"Invalid type: {text_data_json['type']}"
            })
            )
            # TODO recommended message 추가     
    # async def handle_recommended_message(self):
    #     recommended_message = await self.get_query(command_query=self.recommend_message)

    #     await self.send(text_data=json.dumps({
    #         "type":"recommended-message",
    #         "message": recommended_message
    #         })
    #     )
         

    @database_sync_to_async
    def get_room(self) -> ChatRoom | None:
        user:CustomUser =  self.scope['user']
        room_pk = self.scope['url_route']['kwargs']['room_pk']
        room:ChatRoom = None;

        if user.is_authenticated:
            try:
                 room = ChatRoom.objects.get(pk=room_pk)
            except ChatRoom.DoesNotExist:
                  pass
            print("room is not None",room);
            return room
                
    # command_query : 추천 표현 요청 등의 명령어
    # user_query : 사용자 입력
    async def get_query(self, command_query:str=None, user_query:str=None)->str:
        if command_query is not None and user_query is not None:
            raise ValueError("command_query와 user_query 중 하나만 입력해야 합니다.")
        elif command_query is not None:
             self.get_message.append(GptMessage(role="systm",content=command_query))
        elif user_query is not None:
            self.get_message.append(GptMessage(role="user",content=user_query))

        # TODO 랭체인으로 히스토리를 관리하는 것에 대해서 알아보기
        response_message:GptMessage = await self.openai_service.get_chat_response(self.get_message)

        if response_message:
             if command_query is None:
                # connamd query는 추천표현 요청 이기 때문에 get_message에 추가하지 않는다.
                 self.get_message.append(response_message)
             return response_message
        else:
             return "Error: Unable to get response from OpenAI API"


    @database_sync_to_async
    def get_message_count(self, room):
        return room.messages.count()        
    
    @database_sync_to_async
    def save_message(self, room, content):
        message = Message(chat_room=room, content=content)
        message.save()

    @database_sync_to_async
    def save_messages(self,room,messages):
         for message in messages:
              self.save_message(room,message)