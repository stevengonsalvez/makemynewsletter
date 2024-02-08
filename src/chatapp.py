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
import json

warnings.simplefilter("ignore", category=DeprecationWarning)


def load_repo_index():
    directory = "file_db"
    filename = "repo_index.json"
    filepath = os.path.join(directory, filename)
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file does not exist, create it with an empty list
        repo_index = []
        with open(filepath, "w") as file:
            json.dump(repo_index, file)
        return repo_index
    except Exception as e:
        # Handle other exceptions
        raise Exception(f"Failed to load repo index: {str(e)}")


def save_repo_index(index):
    with open("repo_index.json", "w") as file:
        json.dump(index, file)


# Function to create a hash from a given string
def hash_string(string):
    hashed = hex(hash(string))
    return hashed


def get_embedding_function():
    return OpenAIEmbeddings(
        disallowed_special=(), openai_api_key=os.environ.get("OPENAI_API_KEY")
    )


def get_chroma_db(repo_url: str):
    # check if repo has already been processed
    repo_index = load_repo_index()

    if repo_url in repo_index:
        return Chroma(
            persist_directory="output_db", embedding_function=get_embedding_function(), collection_name=hash_string(repo_url)
        )
    else:
        uuid_value = uuid.uuid4()
        repo_path = "/tmp/" + str(uuid_value)
        repo = Repo.clone_from(repo_url, to_path=repo_path)
        loader = GenericLoader.from_filesystem(
            repo_path,
            glob="**/*",
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=20),
        )
        documents = loader.load()
        len(documents)

        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=2000, chunk_overlap=2
        )
        texts = python_splitter.split_documents(documents)
        db = Chroma.from_documents(
            texts,
            get_embedding_function(),
            persist_directory="output_db",
            collection_name=hash_string(repo_url),
        )
        db.persist()

        # Update the repository index
        repo_index.append(repo_url)
        save_repo_index(repo_index)

    return db


def run_llm(vectordb, query: str):
    llm = ChatOpenAI(
        model_name="gpt-4", openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
        memory=memory,
    )
    result = qa(query)
    return result


# Initialize StreamlitChatMessageHistory
msgs = StreamlitChatMessageHistory(key="codebase_chat_history")

# Streamlit UI
st.title("Codebase interaction app")

# Display messages from history
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# user input prompt that will accept a git repository url
git_repo = st.text_input("Enter a git repository url:")


if "clicked" not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


st.button("Run", on_click=click_button)


if st.session_state.clicked:
    if validators.url(git_repo):
        vectordb = get_chroma_db(git_repo)
        query = st.text_input("Ask a question about the codebase:", key="query_input")
        if st.button("Ask"):
            with st.spinner("Generating response..."):
                result = run_llm(vectordb, query)
                st.chat_message("human").write(query)
                st.chat_message("ai").write(str(result))
    else:
        st.write("Please enter a valid git repository url")
