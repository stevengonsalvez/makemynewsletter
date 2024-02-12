import sys, os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb

folder_llm_path = os.path.abspath('./src/LLM')  # Adjust this path as necessary
folder_browser_path = os.path.abspath('./src/Browser')
folder_util_path = os.path.abspath('./src/utils')

# Only append if not already in sys.path
if folder_llm_path not in sys.path:
    sys.path.append(folder_llm_path)
if folder_browser_path not in sys.path:
    sys.path.append(folder_browser_path)
if folder_util_path not in sys.path:
    sys.path.append(folder_util_path)

from LLM import summarize, storage
from Browser import browserfetch
from utils import tools

fetcher = browserfetch.BrowserContentFetcher('safari')
content_list = fetcher.fetch_and_return_all_content()
summarizer = summarize.Summarizer()
storage_obj = storage.Embedder()

for item in content_list:

    # Converting back to a list of one as markdownchunker needs a list
    i_arr = [item]
    summary = summarizer.summarize_markdown_content(i_arr)
    s_arr = tools.generate_tokens(summary)
    storage_obj.embed_document_chroma(s_arr)

print(storage_obj.get_documents())

#chat question to the Llm
question = "is crewAI a platform?"
llm = ChatOpenAI(
            model_name="gpt-4", openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
memory = ConversationSummaryMemory(llm=llm, return_messages=True)
vectorstore = Chroma(persist_directory='output_db', embedding_function=OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ.get("OPENAI_API_KEY")))
qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=memory
        )

result = qa(question)
print (result)