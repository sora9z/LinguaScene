from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from .prompts import SYSTEM_PROMPT_TEMPLATE,USER_PROMPT_TEMPLATE

class ChatCain:
    def __init__(self,api_key):
        self.llm = ChatOpenAI(api_key=api_key,model_name='gpt-3.5-turbo')

    def get_initial_messages(self,context):
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(**context)
        user_prompt = USER_PROMPT_TEMPLATE.format(**context)
        return [
            SystemMessage(context = system_prompt),
            SystemMessage(context = user_prompt)
        ]
    
    def get_response(self, messages):
        response = self.llm.invoke(messages)
        return response
        
    
