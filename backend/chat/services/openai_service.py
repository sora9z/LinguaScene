import os
from typing import List
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

from chat.models import GptMessage
from chat.services.langchain_service.chains import ChatChain


class OpenAiService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_chain = ChatChain(api_key = self.api_key)

    async def get_chat_response(self,messages:List[GptMessage]):
        structured_messages = [
            self._convert_to_langchain_message(message) for message in messages
        ]
        response = self.chat_chain.get_response(structured_messages)
        return  GptMessage(role='assistant', content=response.content)
    
    def _convert_to_langchain_message(self,message:GptMessage):
        if(message['role'] == 'system'):
            return SystemMessage(content=message['content'])
        if(message['role'] == 'user'):
            return HumanMessage(content=message['content'])
        if(message['role'] == 'assistant'):
            return AIMessage(content=message['content'])    