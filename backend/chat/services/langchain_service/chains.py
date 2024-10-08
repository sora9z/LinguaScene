import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from .prompts import SYSTEM_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class ChatChain:
    def __init__(self,api_key):
        self.llm = ChatOpenAI(api_key=api_key,model_name='gpt-3.5-turbo')

    def get_initial_messages(self, context: dict) -> SystemMessage:
        try:
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(**context)
            return SystemMessage(content=system_prompt)
        except Exception as e:
            logger.error(f"[chat/service/openai] error : {e}")
            raise e

    def get_response(self, messages):
        try:
            response = self.llm.invoke(messages)
            return response
        except Exception as e:
            logger.error(f"[chat/service/openai] error in get_response: {e}")
            raise e
