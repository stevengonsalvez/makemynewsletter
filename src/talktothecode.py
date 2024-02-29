from codebase.codebase import CodebaseInteraction
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from src.llm import  vectordb, llm_manager
from config import codebase_llm

llm_mgr = llm_manager.LLMManager(config=codebase_llm)

test = CodebaseInteraction(llm_manager=llm_mgr,repo_url="https://github.com/stevengonsalvez/makemynewsletter")
query = "How do I do a browser fetch for firefox as well, explain with detailed code?"
result = test.retrieval_qa_with_sources(query)
print(result, "\n\n\n")


print (result['result'])
# messages = result['chat_history']

# ai_messages = [ message.content for message in messages if isinstance(message, AIMessage)]

# print(ai_messages)

# query2 = "can you give the full implementation with the packages that need to be used as well?"
# res = test.retrieval_qa_with_sources(query2)

# print(type(res['chat_history']))
# print(f"**Answer**: {res['chat_history']} \n")
# print(f"**Source**: {result['source']} \n")
# print(f"**Source URL**: {result['source_url']} \n")
# print(f"**Source Title**: {result['source_title']} \n")
