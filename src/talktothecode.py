from codebase.codebase import CodebaseInteraction


test = CodebaseInteraction("https://github.com/stevengonsalvez/makemynewsletter")
vectordb = test.get_chroma_db()
query = "How do I refactor the app and implement poetry for dependency management?"
llm, memory = test.get_llm_model()
print(llm, memory)
result = test.retrieval_qa_with_sources(llm, memory, vectordb, query)
print(result)


