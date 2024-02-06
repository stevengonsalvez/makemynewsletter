import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb


class Embedder:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ.get("OPENAI_API_KEY"))
        self.persist_directory = 'output_db'

    def embed_document_chroma(self, doc: [list]):
        "Given a langchain Document, return the embeddings"

        vectordb = Chroma.from_documents(documents=doc, embedding=self.embeddings, persist_directory=self.persist_directory)
        vectordb.persist()
        # return self.embeddings.embed(doc)
    
    def embed_text(self, text: str):
        "Given a text, return the embeddings"
        return self.embeddings.embed_text(text)

    def get_documents(self):
        client = chromadb.Client(Settings(is_persistent=True,
                                    persist_directory= self.persist_directory,
                                ))
        coll = client.get_collection("langchain")
        return coll.get(include=["metadatas"])