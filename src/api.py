from fastapi import FastAPI
from pydantic import BaseModel

from codebase.codebase import CodebaseInteraction
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from src.llm import  vectordb, llm_manager
from config import codebase_llm
import logging, logging.config

# setup logging
# set up logging
logging.config.fileConfig("log.ini")
logger = logging.getLogger("sLogger")


# Define the application instance
app = FastAPI()

# Define the Pydantic model for the chat request
class ChatQuery(BaseModel):
    query: str
    repository: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Revised chat endpoint that uses the ChatQuery model for input
@app.post("/chat/")
async def chat(query: ChatQuery):
    # Here, you would invoke your method using query.query and process the response
    # For demonstration, we'll just echo back the query in a response
    # logger.debug ("entering with query", query.repository)
    response_text = process_query(query.query, query.repository)  # Assume process_query is your method to handle the query
    return {"response": response_text}

# Dummy function to represent processing of the query
def process_query(query_text: str,  repository: str) -> str:
    llm_mgr = llm_manager.LLMManager(config=codebase_llm)
    print("llm manager initiated")
    test = CodebaseInteraction(llm_manager=llm_mgr,repo_url=repository)
    
    result = test.retrieval_qa_with_sources(query_text)
    print(result, "\n\n\n")
    return result['result']