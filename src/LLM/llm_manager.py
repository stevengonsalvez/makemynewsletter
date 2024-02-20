from src.config import llm as llm_config
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from abc import ABC, abstractmethod




class LLMManager:
    def __init__(self):
        self.llm = self.initialize_llm()

    def initialize_llm(self):
        if llm_config["type"] == "openai":
            return OpenAIModel(
                model=llm_config["model"],
                key=llm_config["key"],
                embedding_model=llm_config["embedding_model"],
            )
        # Add initialization for other LLM types as needed
        else:
            raise ValueError("Unsupported LLM type")

    def get_embedding(self):
        return self.llm.get_embedding()

    def get_llm(self):
        return self.llm.get_llm()


class LLMInterface(ABC):

    @abstractmethod
    def get_embedding(self):
        pass

    @abstractmethod
    def get_llm(self):
        pass

class OpenAIModel(LLMInterface):
    def __init__(self, model, key, embedding_model):
        self.model = ChatOpenAI(
            model_name=model,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.key = key
        self.embedding = OpenAIEmbeddings(model=embedding_model, api_key=key)

    def get_embedding(self):
        return self.embedding

    def get_llm(self):
        return self.model





# Similarly, define other service classes as needed, for example, a class for interfacing with a VectorDB like 'Chroma'
