# AI 챗봇 프로젝트

OpenAI API를 사용한 한국어 웹 챗봇입니다. 간단한 UI에서 메시지를 입력하면, 세션별 문맥을 유지하며 자연스럽게 대화합니다. 브라우저에 대화 기록이 저장되어 새로고침 후에도 최근 대화를 확인할 수 있습니다.

## 주요 기능

- 🤖 OpenAI GPT 기반 자연스러운 한국어 대화
- 💬 세션별 문맥 유지 (서버 메모리)
- 💾 브라우저 로컬스토리지 저장으로 새로고침 후에도 기록 유지
- 🧹 "대화 지우기" 버튼 제공
- ⌨️ Enter 전송 / Shift+Enter 줄바꿈
- 📱 반응형 UI

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음과 같이 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
CHATBOT_HOST=127.0.0.1
CHATBOT_PORT=8000
CHATBOT_DEBUG=1
```

### 3. 웹 서버 실행
```bash
python frontend_server.py
```

브라우저에서 다음 주소로 접속하세요:
- 로컬 실행 주소: `http://localhost:8000`
- 배포 주소: `http://43.201.66.249:8000`

### 4. CLI 모드 실행 (선택사항)
```bash
python Chatbot
```

배포 방법 관련 기존 안내는 제거되었습니다.

## 프로젝트 구조

```
python chatbot/
├── chat_backend.py      # 챗봇 핵심 로직
├── frontend_server.py   # Flask 웹 서버
├── Chatbot             # CLI 버전
├── static/
│   └── index.html      # 웹 인터페이스
├── requirements.txt    # Python 의존성
├── Procfile           # 프로세스 정의 (선택)
└── README.md          # 이 파일
```

## 사용법

- 웹 인터페이스에서 메시지를 입력하고 전송 버튼을 클릭하거나 Enter 키를 누르세요
- 대화 기록은 브라우저에 자동으로 저장됩니다
- "대화 지우기" 버튼으로 모든 기록을 삭제할 수 있습니다
- Shift+Enter로 줄바꿈을 입력할 수 있습니다

## 라이센스

MIT License

