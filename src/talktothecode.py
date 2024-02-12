from codebase import CodebaseInteraction

test = CodebaseInteraction("https://github.com/stevengonsalvez/python_training")
vectordb = test.get_chroma_db()
query = "How do I do a file count in python"
result = test.run_llm(vectordb, query)
print(result['answer'])
