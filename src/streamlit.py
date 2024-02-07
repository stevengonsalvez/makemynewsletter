import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import validators
import os
from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


import warnings
import uuid
warnings.simplefilter("ignore", category=DeprecationWarning)


def get_chroma_db(repo_path: str):
    uuid_value = uuid.uuid4()
    repo_path = "/tmp/" + str(uuid_value)
    repo = Repo.clone_from("https://github.com/stevengonsalvez/makemynewsletter", to_path=repo_path)
    loader = GenericLoader.from_filesystem(repo_path, glob="**/*", suffixes=[".py"], parser=LanguageParser(language=Language.PYTHON, parser_threshold=20))
    documents = loader.load()
    len(documents)
    python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=2000, chunk_overlap=2)
    texts = python_splitter.split_documents(documents)
    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=(), openai_api_key=os.environ.get("OPENAI_API_KEY")), persist_directory="output_db")
    db.persist()
    return db

def run_llm(vectordb, query: str ):
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=os.environ.get("OPENAI_API_KEY"))
    memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}), memory=memory)
    result = qa(query)
    return result

# Streamlit UI
st.title("Codebase interaction app")

# user input prompt that will accept a git repository url 
git_repo = st.text_input("Enter a git repository url:")


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button("Run", on_click=click_button)



if st.session_state.clicked:
#     with st.spinner("Generating response..."):
#         if validators.url(git_repo):
#             vectordb = get_chroma_db(git_repo)
#             query = st.text_input("Ask a question about the codebase:")
#             if st.button("Ask"):
#                 result = run_llm(vectordb, query)
#                 st.write(result)
#                 print(result)
#         else:
#             st.write("Please enter a valid git repository url")

        prompt = st.chat_input("Say something")
        if prompt:
            st.write(f"User has sent the following prompt: {prompt}")

