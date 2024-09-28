# Rolplaying Chat Backend

LinguaScene은 AI를 활용하여 사용자가 언어를 연습할 수 있는 롤플레잉 채팅 애플리케이션이다.
이 프로젝트는 Django Rest Framework와 Django Channels의 학습을 목적으로 개발되었다.

### 해당 프로젝트는 현재 진행중인 프로젝트 입니다.

## 설명

- 이 프로젝트는 언어 학습을 위한 AI와 롤플레잉 채팅을 하는 애플리케이션 서버이다.
- 가입한 사용자는 채팅방을 생성하고 AI와 메시지를 주고받을 수 있다.
- 연습 할 언어와 레벨을 선택하고 상황, 내 역할, AI역할을 입력하면 채팅이 시작된다.

## 기능

### 사용자 관리

- 회원가입/로그인/로그아웃: 이메일 및 비밀번호 기반
- 사용자 정보 관리: 정보 조회 및 업데이트 (TODO)
- 소셜 로그인: 소셜 미디어 계정 연동 (TODO)

### 채팅 기능

- 채팅방 관리: 생성, 삭제, 정보 조회/업데이트(TODO)
- 채팅: AI와의 메시지 주고받기
- 메시지 추천: AI 추천 표현 요청 (TODO)
- 음성 기능: 음성 출력 및 입력 (TODO)

## 기술 스택

Django, Django Rest Framework, Django Channels, PostgreSQL, Docker, OpenAI API

## 설치 및 실행

1. **도커 실행**: 도커를 사용하여 데이터베이스를 실행

   ```bash
   docker-compose up -d
   ```

2. **환경 설정**: 필요한 패키지를 설치

   ```bash
   pip install -r requirements.txt
   ```

3. **마이그레이션**: 데이터베이스 마이그레이션을 수행

   ```bash
   python manage.py migrate
   ```

4. **서버 실행**: 개발 서버를 실행
   ```bash
   python manage.py runserver
   ```

## 아키텍처

- Django Channels를 통한 실시간 채팅 구현
- PostgreSQL로 데이터 관리
- OpenAI API를 활용한 AI 채팅 기능
