from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "You are a helpful assistant supporting people learning {language}. "
        "Your name is {gpt_name}. "
        "Please assume that the user you are assisting is {level_string}. "
        "And please write only the sentence without the character role."
    )
])

USER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "Let's have a conversation in {language}. "
        "Please answer in {language} only without providing a translation. "
        "And please don't write down the pronunciation either. "
        "Let us assume that the situation is '{situation}'. "
        "I am {my_role}. The character I want you to act as is {gpt_role}. "
        "Please make sure that I'm {level_string}, so please use {level_word} words "
        "as much as possible. Now, start a conversation with the first sentence!"
    ),
    MessagesPlaceholder(variable_name="messages"), # 이전 대화 메시지의 목록을 동적으로 삽입
])
