import os
from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings
import uuid
import json
import utils.prompts as prompts
from src.llm.llm_manager import LLMManager
from src.llm.vectordb import VectordbManager
from src.config import codebase_vectordb

warnings.simplefilter("ignore", category=DeprecationWarning)


class CodebaseInteraction:
    def __init__(
        self,
        repo_url: str = None,
        config_db=codebase_vectordb,
        llm_manager: LLMManager = None,
    ):
        self.repo_url = repo_url
        self.config_db = config_db
        self.llm_manager = llm_manager

        default_vector_dbconfig = dict(
                type=self.config_db["type"],
                persist_directory=self.config_db["persist_directory"],
                collection_name=self.extract_repo_name(),
            )
        
        
        self.storage_obj = VectordbManager(config=default_vector_dbconfig,llm_manager=self.llm_manager)

 

        self.repo_index_directory = "file_db"
        self.repo_index_filename = "repo_index.json"
        self.repo_index_filepath = os.path.join(
            self.repo_index_directory, self.repo_index_filename
        )
        self.repo_index = self.load_repo_index()
        self.embedding_function = self.llm_manager.get_embedding()

       ## initiating storage of code in vectordbmanager
        _ = self.get_chroma_db()
        
        # memory = ConversationSummaryMemory(
        #     llm=llm, memory_key="chat_history", return_messages=True
        # )
        # due to this error need to use multiple keys
        # https://github.com/langchain-ai/langchain/issues/2256#issuecomment-1645351967
        self.memory = ConversationBufferMemory(
            llm=self.llm_manager.get_llm(),
            memory_key="chat_history",
            return_messages=True,
            input_key="query",
            output_key="result",
        )

    def load_repo_index(self):
        # Ensure the directory exists
        os.makedirs(self.repo_index_directory, exist_ok=True)

        try:
            if (
                os.path.exists(self.repo_index_filepath)
                and os.path.getsize(self.repo_index_filepath) > 0
            ):
                with open(self.repo_index_filepath, "r") as file:
                    return json.load(file)
            else:
                # If the file does not exist or is empty, create it with an empty list
                repo_index = []
                with open(self.repo_index_filepath, "w") as file:
                    json.dump(repo_index, file)
                return repo_index
        except Exception as e:
            # Handle other exceptions
            raise Exception(f"Failed to load repo index: {str(e)}")

    def save_repo_index(self):
        with open(self.repo_index_filepath, "w") as file:
            print(self.repo_index_filepath)
            json.dump(self.repo_index, file)

    # Function to extract the last part of a github repo url string
    def extract_repo_name(self):
        repo_name = self.repo_url.split("/")[-1]
        return repo_name

    # Function to create a hash from a given string
    def hash_string(self, string):
        hashed = hex(hash(self.extract_repo_name()))
        return hashed

    def get_chroma_db(self):
        # check if repo has already been processed
        if self.repo_url in self.repo_index:
            return self.storage_obj.get_db()
        else:
            uuid_value = uuid.uuid4()
            repo_path = "/tmp/" + str(uuid_value)
            repo = Repo.clone_from(self.repo_url, to_path=repo_path)
            loader = GenericLoader.from_filesystem(
                repo_path,
                glob="**/*",
                suffixes=[".py"],
                parser=LanguageParser(language=Language.PYTHON, parser_threshold=20),
            )
            documents = loader.load()
            len(documents)

            python_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=2000, chunk_overlap=2
            )
            texts = python_splitter.split_documents(documents)
            db = self.storage_obj.get_db().from_documents(
                texts,
                self.embedding_function,
                persist_directory="output_db",
                collection_name=self.extract_repo_name(),
            )
            # db.persist()

            # Update the repository index
            self.repo_index.append(self.repo_url)
            self.save_repo_index()

        return db

    def conversational_chat_llm(self, query: str):

        qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm_manager.get_llm(),
            retriever=self.storage_obj.get_db().as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=self.memory,
        )
        result = qa(query)
        return result

    def retrieval_qa_with_sources(self, query: str):

        chain_type_kwargs = {
            "prompt": prompts.get_codeqa_prompt_hub(),
        }

        qa = RetrievalQA.from_chain_type(
            llm=self.llm_manager.get_llm(),
            chain_type="stuff",
            retriever=self.storage_obj.get_db().as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=self.memory,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
        )
        result = qa({"query": query})
        return result
