import logging
import os
from typing import List
from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError
from dotenv import load_dotenv

from chat.models import GptMessage

logger = logging.getLogger(__name__)
load_dotenv()

class OpenAiService:

    def __init__(self):
          # OpenAI API 키 설정
        self.api_key = os.getenv("OPENAI_API_KEY") 
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def get_chat_response(self, get_message: List[GptMessage])  -> GptMessage:
        """
        OpenAI의 ChatCompletion API에 요청을 보내고 응답을 받는다
        """
        try:
            
            response_dict = await self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages= get_message,
                temperature=1 # 0-1 범위의 실수값. 최대값인 1로 지정해서 무작위성을 최대한 높임)
            )  

            response_role = response_dict.choices[0].message.role
            response_message = response_dict.choices[0].message.content

            return GptMessage(role=response_role, content=response_message)
        except APIConnectionError as e:
            logger.error("The server could not be reached",e)
        except RateLimitError as e:
            logger.error("A 429 status code was received; we should back off a bit.",e)
        except APIStatusError as e:
            logger.error("Another non-200-range status code was received",e)


