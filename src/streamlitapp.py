import streamlit as st
import validators
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from codebase.codebase import CodebaseInteraction


# Initialize StreamlitChatMessageHistory
msgs = StreamlitChatMessageHistory(key="codebase_chat_history")

# Streamlit UI
st.title("Codebase interaction app")

# Display messages from history
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# user input prompt that will accept a git repository url
git_repo = st.text_input("Enter a git repository url:")
codebase = CodebaseInteraction(git_repo)
print (codebase.repo_index)

if "clicked" not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


st.button("Run", on_click=click_button)

print("repository", git_repo)   
if st.session_state.clicked:
    if validators.url(git_repo):
        vectordb = codebase.get_chroma_db()
        query = st.text_input("Ask a question about the codebase:", key="query_input")
        if st.button("Ask"):
            with st.spinner("Generating response..."):
                print ("query", query)
                result = codebase.run_llm(vectordb, query)
                st.chat_message("human").write(query)
                st.chat_message("ai").write(str(result))
    else:
        st.write("Please enter a valid git repository url")

