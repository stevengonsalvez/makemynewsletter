from src.config import vectordb as vectordb_config
from abc import ABC, abstractmethod
from chromadb.config import Settings
import chromadb
from chromadb.utils import embedding_functions
from chromadb.db.base import UniqueConstraintError
from src.llm.llm_manager import LLMManager
from langchain_community.vectorstores import Chroma
import chromadb.utils.embedding_functions as embedding_functions


class VectordbManager:
    def __init__(self, config=vectordb_config, llm_manager=None):
        self.llm_manager = llm_manager
        self.config = config
        self.vectordb = self.load_vectordb()

    def load_vectordb(self):
        if self.config["type"] == "chroma":
            return ChromaVectordb(self.config, self.llm_manager)
        else:
            raise ValueError("Unsupported Vectordb type")

    def get_documents(self):
        return self.vectordb.get_documents()

    def embed_documents(self, documents: list):
        return self.vectordb.embed_documents(documents)

    def get_db(self):
        return self.vectordb.get_db()


class IVectordb(ABC):
    @abstractmethod
    def get_documents(self):
        pass

    @abstractmethod
    def embed_documents(self, documents):
        pass

    @abstractmethod
    def get_db(self):
        pass


class ChromaVectordb(IVectordb):
    def __init__(self, config=None, llm_manager=None):
        self.config = config
        self.persist_directory = config.get("persist_directory", "output_db")
        self.collection_name = config.get("collection_name", "langchain")
        # Assuming the embedding creation logic is moved to a common place accessible here
        self.llm_manager = llm_manager
        self.embeddings = self.llm_manager.get_embedding()
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        self._create_collection()

    def _create_collection(self):
        # Implementation for creating a collection
        try:
            self.chroma_client.create_collection(self.collection_name)
        except UniqueConstraintError:
            pass

    def get_db(self):
        # Implementation for returning the langchain chroma client
        langchain_chromadb = Chroma(
            client=self.chroma_client,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )
        return langchain_chromadb

    def get_documents(self):

        coll = self.chroma_client.get_collection(self.collection_name)
        return coll.get(include=["metadatas"])

    def embed_documents(self, documents):
        self.get_db().from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
        )
        # self.get_db().persist()


# test_llm = LLMManager()
# print(LLMManager().get_embedding())
# # vectordb_manager = VectordbManager(llm_manager=test_llm)
