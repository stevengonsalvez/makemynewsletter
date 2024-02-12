import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb


class Embedder:
    def __init__(self, collection_name: str = "langchain"):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.collection_name = collection_name
        self.persist_directory = "output_db"

    def embed_document_chroma(self, doc: [list]):
        "Given a langchain Document, return the embeddings"

        vectordb = Chroma.from_documents(
            documents=doc,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        vectordb.persist()

    def embed_text(self, text: str):
        "Given a text, return the embeddings"
        return self.embeddings.embed_text(text)

    def get_documents(self):
        client = chromadb.Client(
            Settings(
                is_persistent=True,
                persist_directory=self.persist_directory,
            )
        )
        coll = client.get_collection(self.collection_name)
        return coll.get(include=["metadatas"])

    def get_db(self):
        return Chroma(
            persist_directory=self.persist_directory, embedding=self.embeddings, collection_name=self.collection_name
        )
