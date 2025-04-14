# MetaSeminar Master Chatbot

기본적인 설치법은 아래 적어두었습니다. 
프로젝트가 chat, llm, config 로 구성되어 있지만 실제로 구현되는 부분은
chat.py의 


에이아이 응답부분
ai_message = st.write_stream(ai_response)

ai_response는 llm.py 의 가장 마지막에서 임포트해서 사용하고 있습니다.

사용자의 질문 부분
if user_question := st.chat_input(placeholder="질문을 입력하세요"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role":"user","content":user_question})

입니다.

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



### Flask

플라스크로 기존 퍼브리싱에 적용해보았습니다.
pip install flask==3.0.2 flask-socketio==5.3.6

혹시나 잘 안되면 아래 렝체인 설치
pip install langchain langchain_core langchain_openai langchain_pinecone langchain_community

실행
python app.py 



