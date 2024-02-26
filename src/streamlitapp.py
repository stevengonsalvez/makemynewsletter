import streamlit as st
import validators
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from codebase.codebase import CodebaseInteraction
from llm import llm_manager
from config import codebase_llm
llm_mgr = llm_manager.LLMManager(config=codebase_llm)


# Streamlit UI
st.title("Codebase interaction app")
msgs = StreamlitChatMessageHistory()


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

if st.session_state.clicked:
    if validators.url(git_repo):
        codebase =  CodebaseInteraction(llm_manager=llm_mgr,repo_url=git_repo)
        print (codebase.repo_index, "repo index")
        query = st.text_input("Ask a question about the codebase:", key="query_input")
        if st.button("Ask"):
            with st.spinner("Generating response..."):
                print ("query", query)
                result = codebase.retrieval_qa_with_sources(query)
                st.chat_message("human").write(query)
                st.chat_message("ai").write(str(result))
    else:
        st.write("Please enter a valid git repository url")

