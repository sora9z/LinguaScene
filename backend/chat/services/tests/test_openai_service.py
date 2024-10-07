
from unittest.mock import patch

from chat.services.openai_service import OpenAiService


class OPenAIServiceTestCase:

    # api key를 로드하는가
    # chat_chain을 사용해서 메시지에 대한 응답을 받는가
    # chat_chain의 method를 모의하여 예상대로 응답을 처리하는지 확인
    @patch('chat.services.langchain_service.chains.ChatChain')
    @patch('os.getenv')
    async def test_get_chat_response(mock_getenv,mock_chat_chain):
        mock_getenv.return_value = 'test_api_key'
        mock_chat_chain_instance = mock_chat_chain.return_value
        mock_chat_chain_instance.get_response.return_value = 'mocked response'

        service = OpenAiService()
        messages = [{'role':'user','content':'hello'}]
        response = service.def_chat_response(messages)

        # assertion
        mock_getenv.assert_called_once_with("OPENAI_API_KEY")
        mock_chat_chain.assert_called_once_with(api_key='test_api_key')
        mock_chat_chain_instance.get_response.assert_called_once_with(messages)
        assert response == 'mocked response'