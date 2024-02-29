import streamlit as st
import validators
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from codebase.codebase import CodebaseInteraction
from llm import llm_manager
from config import codebase_llm
import logging, logging.config
# set up logging
logging.config.fileConfig("log.ini")
logger = logging.getLogger("sLogger")


llm_mgr = llm_manager.LLMManager(config=codebase_llm)


# Streamlit UI
st.title("Codebase interaction app")
msgs = StreamlitChatMessageHistory(key="langchain_messages")
view_messages = st.expander("View the message contents in session state")

git_repo = st.text_input("Enter a git repository url:") 

if "clicked" not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True
    # user input prompt that will accept a git repository url

st.button("Run", on_click=click_button)


# Display messages from history
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.clicked:
    if validators.url(git_repo):
        codebase =  CodebaseInteraction(llm_manager=llm_mgr,repo_url=git_repo)
        logger.debug(codebase.repo_index, "repo index")
        query = st.chat_input("Ask a question about the codebase:", key="query_input")
        if query:
            with st.spinner("Generating response..."):
                logger.debug("query", query)
                st.chat_message("human").write(query)
                # Note: new messages are saved to history automatically by Langchain during run
                config = {"configurable": {"session_id": "any"}}
                result = codebase.retrieval_qa_with_sources(query)
                st.chat_message("ai").write(result['result'])
                st.session_state.messages.append({"role": "user", "content": query})
    else:
        st.write("Please enter a valid git repository url")

with view_messages:
    """
    Message History initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)