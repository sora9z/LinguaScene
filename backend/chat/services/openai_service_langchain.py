import os

from chat.services.langchain_service.chains import ChatCain


class OPenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_chain = ChatCain(api_key = self.api_key)

    async def def_chat_response(self,messages):
        response = self.chat_chain.get_response(messages)
        return response