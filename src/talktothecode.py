from codebase.codebase import CodebaseInteraction
from src.llm import  vectordb, llm_manager
from config import codebase_llm

llm_mgr = llm_manager.LLMManager(config=codebase_llm)
storage_obj = vectordb.VectordbManager(llm_manager=llm_mgr)


test = CodebaseInteraction(llm_manager=llm_mgr,repo_url="https://github.com/stevengonsalvez/makemynewsletter")
query = "How do I refactor the app and implement poetry for dependency management?"
result = test.retrieval_qa_with_sources(query)
print(result)


