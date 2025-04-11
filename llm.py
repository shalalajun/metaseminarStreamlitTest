from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA


def get_ai_message(user_message):
  
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    index_name='metaseminar01'
    database = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embedding
    )

    llm = ChatOpenAI(model = 'gpt-4o')
    prompt = hub.pull("rlm/rag-prompt")
    retriever = database.as_retriever(search_kwargs={"k": 4})
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt":prompt}
    )

    dictionary = ["메타버스 -> 메타세미나"]

    prompt = ChatPromptTemplate.from_template(f"""사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요 만약 변경할 필요가 없다고 판단되면, 사용자의 질문을 변경해도 됩니다. 그런 경우에는 질문만 리턴해 주세요.
    사전:{dictionary}

    질문: {{question}}
    """)

    dictionary_chain = prompt | llm | StrOutputParser()
    last_chain = {"query":dictionary_chain} | qa_chain

    ai_message = last_chain.invoke({"question":user_message})
    return ai_message["result"]