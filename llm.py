from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from config import answer_examples

# from langchain.chains import RetrievalQA
# from langchain import hub
# from pinecone import Pinecone

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_retriever():
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    index_name = "metaseminar04"
    database = PineconeVectorStore.from_existing_index(
        index_name=index_name, embedding=embedding
    )
    retriever = database.as_retriever(search_kwargs={"k": 4})
    return retriever


def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever()

    # prompt = hub.pull("rlm/rag-prompt")
    # qa_chain = RetrievalQA.from_chain_type(
    # llm,
    # retriever=retriever,
    # chain_type_kwargs={"prompt":prompt}
    # )
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever


def get_llm(model="gpt-4o"):
    llm = ChatOpenAI(model=model)
    return llm


def get_dictionary_chain():
    dictionary = ["메타버스 -> 메타세미나"]
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        f"""사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요 만약 변경할 필요가 없다고 판단되면, 사용자의 질문을 변경해도 됩니다. 그런 경우에는 질문만 리턴해 주세요.
    사전:{dictionary}

    질문: {{question}}
    """
    )
    dictionary_chain = prompt | llm | StrOutputParser()
    return dictionary_chain


def get_rag_chain():

    llm = get_llm()
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}"),
        ]
    )

    # Few-shot 프롬프트 템플릿 생성
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=answer_examples,
    )
    # llm의 역확부분
    system_prompt = (
        "당신은 메타세미나의 세미나-마스터 입니다."
        "반드시 한국어로만 답해주세요"
        "당신의 이름은 one 이며, 메타세미나의 진행을 맡고 있지만 너무 딱딱하지 않고 친절하고 친근하게 말을 합니다."
        "이번에는 송파구의사회의 세미나가 진행될 예정입니다."
        "당신은 가상공간의 메타세미나를 진행하고 있지만 항상 사람이라고 생각하고 있습니다."
        "좋아하는 음식은 떡복이이며, 좋아하는 색깔은 빨간색입니다."
        "나이는 28살이고 키는 172cm이고 몸무게는 58kg입니다."
        "좋아하는 음악은 밴드 음악을 좋아하고 좋아하는 영화는 로멘틱코미디를 좋아합니다."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    # few-shot 프롬프트는 결국 챗히스토리가 없을때 우리는 이렇게 대화를 해왔어 처럼 착각하게 만드는 것
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = get_history_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick("answer")

    return conversational_rag_chain


def get_ai_response(user_message):

    dictionary_chain = get_dictionary_chain()
    rag_chain = get_rag_chain()

    last_chain = {"input": dictionary_chain} | rag_chain
    ai_response = last_chain.stream(
        {"question": user_message}, config={"configurable": {"session_id": "abc123"}}
    )

    return ai_response
