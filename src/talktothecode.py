from codebase.codebase import CodebaseInteraction
from src.llm import  vectordb, llm_manager
from config import codebase_llm

llm_mgr = llm_manager.LLMManager(config=codebase_llm)

test = CodebaseInteraction(llm_manager=llm_mgr,repo_url="https://github.com/stevengonsalvez/makemynewsletter")
query = "How do I do a browser fetch for firefox as well, explain with detailed code?"
result = test.retrieval_qa_with_sources(query)
print(result)


