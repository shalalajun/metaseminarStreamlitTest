import streamlit as st

from dotenv import load_dotenv

from llm import get_ai_message

load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")
st.title("metaSeminar Master")
st.caption("메타세미나 마스터 챗봇")

# 채팅 인풋 질문
# user_question = st.chat_input(placeholder="질문을 입력하세요")
# if user_question:
# pass
# := 는 새로운 파이썬 연산자 참고,
# placeholder 는 스트림릿의 chat_input 함수에서 사용하는 매개변수

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])



if user_question := st.chat_input(placeholder="질문을 입력하세요"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role":"user","content":user_question})

    with st.spinner("생각중입니다."):
        ai_message = get_ai_message(user_question)
        with st.chat_message("ai"):
            st.write(ai_message)
        st.session_state.message_list.append({"role":"ai","content":ai_message})




