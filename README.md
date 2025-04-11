# MetaSeminar Master Chatbot

메타세미나 마스터 챗봇은 LangChain과 Streamlit을 사용하여 개발된 AI 챗봇입니다.

## 🚀 시작하기

### 필수 조건
- Python 3.10 이상
- OpenAI API 키
- Pinecone API 키

### 설치 방법

1. 가상환경 생성 및 활성화
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
# 또는
.\env\Scripts\activate  # Windows
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### 실행 방법

1. Streamlit 앱 실행
```bash
streamlit run chat.py
```

2. 웹 브라우저에서 접속
- Streamlit이 자동으로 기본 브라우저를 열어줍니다
- 또는 수동으로 `http://localhost:8501` 주소로 접속할 수 있습니다
