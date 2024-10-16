from typing import Literal

from bs4 import BeautifulSoup
import requests


def google_translate(
    text: str, source: Literal["auto", "en", "ko"], target: Literal["en", "ko"]
) -> str:
    text = text.strip()

    if not text:
        return ""

    endpoint_url = "https://translate.google.com/m"
    params = {
        "hl": source,  #  원본 텍스트의 언어 코드
        "sl": source,  # 원본 텍스트의 언어 코드
        "tl": target,  # 번역할 대상 언어의 코드
        "q": text,  # 번역할 실제 텍스트
        "ie": "UTF-8",  # 입력 텍스트의 문자 인코딩
        "prev": "_m",  # 이전 페이지의 정보
    }

    headers = {
        # 모바일 흉내내기
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36"
        )
    }

    try:
        res = requests.get(
            endpoint_url,
            params=params,
            headers=headers,
            timeout=5,
        )

        res.raise_for_status()

        # HTML 또는 XML 문서를 파싱하여 BeautifulSoup 객체로 반환한다. 이를 통해 HTML문서의 특정 요소를 쉽게 조작 가능
        soup = BeautifulSoup(res.text, "html.parser")
        translated_text = soup.select_one(".result-container").text.strip()
        return translated_text
    except Exception as e:
        print(f"[chat/service/get] error: {e}")
        # logger.error(f"[chat/service/get] error: {e}")
        raise e
