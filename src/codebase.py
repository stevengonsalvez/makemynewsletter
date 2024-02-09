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
import json

warnings.simplefilter("ignore", category=DeprecationWarning)


warnings.simplefilter("ignore", category=DeprecationWarning)


class CodebaseInteraction:
    def __init__(self):
        self.repo_index_directory = "file_db"
        self.repo_index_filename = "repo_index.json"
        self.repo_index_filepath = os.path.join(self.repo_index_directory, self.repo_index_filename)
        self.repo_index = self.load_repo_index()

    def load_repo_index(self):
        # Ensure the directory exists
        os.makedirs(self.repo_index_directory, exist_ok=True)

        try:
            if os.path.exists(self.repo_index_filepath) and os.path.getsize(self.repo_index_filepath) > 0:
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

    # Function to create a hash from a given string
    def hash_string(self, string):
        hashed = hex(hash(string))
        return hashed

    def get_embedding_function(self):
        return OpenAIEmbeddings(
            disallowed_special=(), openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

    def get_chroma_db(self, repo_url: str):
        # check if repo has already been processed
        if repo_url in self.repo_index:
            return Chroma(
                persist_directory="output_db",
                embedding_function=self.get_embedding_function(),
                collection_name=self.hash_string(repo_url),
            )
        else:
            uuid_value = uuid.uuid4()
            repo_path = "/tmp/" + str(uuid_value)
            repo = Repo.clone_from(repo_url, to_path=repo_path)
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
            db = Chroma.from_documents(
                texts,
                self.get_embedding_function(),
                persist_directory="output_db",
                collection_name=self.hash_string(repo_url),
            )
            db.persist()

            # Update the repository index
            self.repo_index.append(repo_url)
            self.save_repo_index()

        return db

    def run_llm(self, vectordb, query: str):
        llm = ChatOpenAI(
            model_name="gpt-4", openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=memory,
        )
        result = qa(query)
        return result


