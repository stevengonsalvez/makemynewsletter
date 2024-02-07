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

uuid_value = uuid.uuid4()


repo_path = "/tmp/" + str(uuid_value)
repo = Repo.clone_from("https://github.com/stevengonsalvez/makemynewsletter", to_path=repo_path)


loader = GenericLoader.from_filesystem(repo_path, glob="**/*", suffixes=[".py"], parser=LanguageParser(language=Language.PYTHON, parser_threshold=20))
documents = loader.load()
len(documents)

python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=2000, chunk_overlap=2)
texts = python_splitter.split_documents(documents)

db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=(), openai_api_key=os.environ.get("OPENAI_API_KEY")))
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=os.environ.get("OPENAI_API_KEY"))
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)

question = " can you show me few parts of the code that I can refactor?"
result = qa(question)
print(result)

