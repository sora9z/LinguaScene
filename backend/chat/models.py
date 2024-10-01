import os
from typing import Literal, TypedDict, List
from django.db import models

from .services.langchain_service.chains import ChatChain
# TypedDict은 사전으로 사용이 되지만 타입으로도 지정할 수 있다.
class GptMessage(TypedDict):
    role: Literal["system", "user","assistant"]
    content:str

class ChatRoom(models.Model):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.chat_chain = ChatChain(api_key=os.getenv("OPENAI_API_KEY"))
    class Language(models.TextChoices):
        # 코드에서 사용, 데이터베이스에 저장, 사용자에게 보여지는 값
        ENGLISH = 'en-US', 'English'
        KOREAN = 'ko-KR', 'Korean'
        JAPANESE = 'ja-JP', 'Japanese'
        CHINESE = 'zh-CN', 'Chinese'
        SPANISH = 'es-ES', 'Spanish'
        FRENCH = 'fr-FR', 'French'
        GERMAN = 'de-DE', 'German'
        ITALIAN = 'it-IT', 'Italian'
        PORTUGUESE = 'pt-PT', 'Portuguese'
        RUSSIAN = 'ru-RU', 'Russian'
        THAI = 'th-TH', 'Thai'
    
    class Level(models.IntegerChoices):
        BEGINNER = 1, 'Beginner'
        INTERMEDIATE = 2, 'Intermediate'
        ADVANCED = 3, 'Advanced'
    
    class Meta:
        ordering = ["-pk"] # 이 모델로부터 사행되는 QuerySet에 기본 정렬방향 지정. pk의 역순 정렬

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='채팅방 이름')
    language = models.CharField(
        max_length = 10,
        choices = Language.choices,
        default = Language.ENGLISH,
        verbose_name = '언어',
    )
    level = models.IntegerField(
        choices = Level.choices,
        default = Level.BEGINNER,
        verbose_name = '레벨',
    )
    situation = models.CharField(max_length=100, verbose_name='상황')
    situation_en = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='상황 영문',
        help_text='GPT 프롬프트에 직접적으로 활용됨. 비어있는 경우 situation 필드를 번역하여 자동으로 반영됨.',
        )
    my_role = models.CharField(max_length=100, verbose_name='나의 역할')
    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='나의 역할 영문',
        help_text='GPT 프롬프트에 직접적으로 활용됨. 비어있는 경우 my_role 필드를 번역하여 자동으로 반영됨.',
    )
    gpt_role = models.CharField(max_length=100, verbose_name='GPT 역할')
    gpt_role_en = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='GPT 역할 영문',
        help_text='GPT 프롬프트에 직접적으로 활용됨. 비어있는 경우 gpt_role 필드를 번역하여 자동으로 반영됨.',
    )

    def get_level_string(self):
        if self.level == self.Level.BEGINNER:
            return f"a beginner in {self.get_language_display()}"
        elif self.level == self.Level.INTERMEDIATE:
            return f"an intermediate learner in {self.get_language_display()}"
        elif self.level == self.Level.ADVANCED:
            return f"an advanced learner in {self.get_language_display()}"
        else:
            raise ValueError(f"Invalid level: {self.level}")
        
    def get_level_word(self):
        if self.level == self.Level.BEGINNER:
            return "very simple"
        elif self.level == self.Level.INTERMEDIATE:
            return "simple"
        elif self.level == self.Level.ADVANCED:
            return "complex"
        else:
            raise ValueError(f"Invalid level: {self.level}")                

    def get_initial_messages(self)->List[GptMessage]:
        
        context = {
            "gpt_name": "RolePlayingBot",
            "language": self.get_language_display(),
            "situation": self.situation_en or self.situation,
            "my_role": self.my_role_en or self.my_role,
            "gpt_role": self.gpt_role_en or self.gpt_role,
            "level_string": self.get_level_string(),
            "level_word": self.get_level_word(),
        }
        initial_messages = self.chat_chain.get_initial_messages(context)
        return initial_messages

    # TODO
    # def get_recommend_message(self)->str:
    #     level = self.level

    #     if level == self.Level.BEGINNER:
    #         level_word = "very simple"
    #     elif level == self.Level.INTERMEDIATE:
    #         level_word = "simple"
    #     elif level == self.Level.ADVANCED:
    #         level_word = "difficult"
    #     else:
    #         raise ValueError(f"Invalid level : {level}")
    #     return (
    #         f"Can you please provide me an {level_word} example "
    #         f"of how to respond to the last sentence "
    #         f"in this situation, without providing a translation "
    #         f"and any introductory phrases or sentences."
    #     )


    

