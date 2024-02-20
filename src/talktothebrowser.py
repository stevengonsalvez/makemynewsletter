import sys, os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory


from src.browser import browserfetch
from src.llm import summarize, vectordb, llm_manager
from src.utils import tools

fetcher = browserfetch.BrowserContentFetcher('safari')
content_list = fetcher.fetch_and_return_all_content()
llm_mgr = llm_manager.LLMManager()


summarizer = summarize.Summarizer(llm_manager=llm_mgr)
storage_obj = vectordb.VectordbManager(llm_manager=llm_mgr)

for item in content_list:

    # Converting back to a list of one as markdownchunker needs a list
    i_arr = [item]
    summary = summarizer.summarize_markdown_content(i_arr)
    s_arr = tools.generate_tokens(summary)
    storage_obj.embed_documents(s_arr)

print(storage_obj.get_documents())

#chat question to the Llm
question = "is crewAI a platform?"
llm = llm_mgr.get_llm()
memory = ConversationSummaryMemory(memory_key="chat_history",
                                    llm=llm, return_messages=True)
vectorstore = storage_obj.get_db()
qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=memory
        )

result = qa(question)
print (result)