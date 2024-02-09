import streamlit as st
import validators
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from codebase import CodebaseInteraction


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
        vectordb = CodebaseInteraction.get_chroma_db(git_repo)
        query = st.text_input("Ask a question about the codebase:", key="query_input")
        if st.button("Ask"):
            with st.spinner("Generating response..."):
                result = CodebaseInteraction.run_llm(vectordb, query)
                st.chat_message("human").write(query)
                st.chat_message("ai").write(str(result))
    else:
        st.write("Please enter a valid git repository url")