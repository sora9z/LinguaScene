import os
from typing import List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from chat.models import GptMessage
from chat.services.langchain_service.chains import ChatChain


class OpenAiService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_chain = ChatChain(api_key=self.api_key)

    async def get_initial_response(self, init_setting) -> dict[GptMessage, GptMessage]:
        initial_message = self.chat_chain.get_initial_messages(init_setting)
        initial_message_content = initial_message.content
        response = await self._get_response([initial_message])
        return {
            "initial_message": GptMessage(
                role="system", content=initial_message_content
            ),
            "response": response,
        }

    async def get_chat_response(self, messages: List[GptMessage]):

        structured_messages = [
            self._convert_to_langchain_message(message) for message in messages
        ]
        return await self._get_response(structured_messages)

    def _convert_to_langchain_message(self, message: GptMessage):
        if message["role"] == "system":
            return SystemMessage(content=message["content"])
        if message["role"] == "user":
            return HumanMessage(content=message["content"])
        if message["role"] == "assistant":
            return AIMessage(content=message["content"])

    async def _get_response(self, messages) -> GptMessage:
        response = self.chat_chain.get_response(messages)
        return GptMessage(role="assistant", content=response.content)
