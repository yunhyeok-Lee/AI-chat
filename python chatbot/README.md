# AI 챗봇 프로젝트

OpenAI API를 사용한 한국어 AI 챗봇입니다. 웹 인터페이스와 CLI 모드를 모두 지원합니다.

## 주요 기능

- 🤖 OpenAI GPT를 사용한 자연스러운 한국어 대화
- 💬 대화 문맥 유지 (세션별 메모리)
- 🌐 깔끔한 웹 인터페이스
- 💾 브라우저 로컬스토리지를 통한 대화 기록 저장
- 🚀 AWS 배포 지원
- 📱 반응형 디자인

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

브라우저에서 `http://localhost:8000`에 접속하세요.

### 4. CLI 모드 실행 (선택사항)
```bash
python Chatbot
```

## AWS 배포

### Heroku 배포
1. Heroku CLI 설치 및 로그인
2. 새 앱 생성: `heroku create your-chatbot-app`
3. 환경 변수 설정: `heroku config:set OPENAI_API_KEY=your_key`
4. 배포: `git push heroku main`

### AWS EC2 배포
1. EC2 인스턴스 생성 (Ubuntu 20.04 권장)
2. 필요한 패키지 설치:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```
3. 프로젝트 클론 및 설정:
   ```bash
   git clone your-repo-url
   cd python-chatbot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. 환경 변수 설정 후 실행:
   ```bash
   export OPENAI_API_KEY=your_key
   export CHATBOT_HOST=0.0.0.0
   export CHATBOT_PORT=80
   python frontend_server.py
   ```

## 프로젝트 구조

```
python chatbot/
├── chat_backend.py      # 챗봇 핵심 로직
├── frontend_server.py   # Flask 웹 서버
├── Chatbot             # CLI 버전
├── static/
│   └── index.html      # 웹 인터페이스
├── requirements.txt    # Python 의존성
├── Procfile           # Heroku 배포용
└── README.md          # 이 파일
```

## 사용법

- 웹 인터페이스에서 메시지를 입력하고 전송 버튼을 클릭하거나 Enter 키를 누르세요
- 대화 기록은 브라우저에 자동으로 저장됩니다
- "대화 지우기" 버튼으로 모든 기록을 삭제할 수 있습니다
- Shift+Enter로 줄바꿈을 입력할 수 있습니다

## 라이센스

MIT License
