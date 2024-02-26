from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl
# The line `from src.codebase import CodebaseInteraction` is importing the `CodebaseInteraction` class
# from a module named `codebase` located in a directory named `src`. This allows the code to access
# and use the functionalities provided by the `CodebaseInteraction` class within the current script or
# module.
# from src.codebase import CodebaseInteraction




from chainlit.input_widget import TextInput


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            TextInput(id="AgentName", label="Agent Name", initial="AI"),
        ]
    ).send()
    value = settings["AgentName"]


# @cl.on_chat_start
# async def start():
#     chain = qa_bot()
#     msg = cl.Message(content="Firing up the research info bot...")
#     await msg.send()
#     msg.content = "Hi, welcome to research info bot. What is your query?"
#     await msg.update()
#     cl.user_session.set("chain", chain)


# @cl.on_message
# async def main(message):
#     chain = cl.user_session.get("chain")
#     cb = cl.AsyncLangchainCallbackHandler(
#         stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
#     )
#     cb.answer_reached = True
#     # res=await chain.acall(message, callbacks=[cb])
#     res = await chain.acall(message.content, callbacks=[cb])
#     print(f"response: {res}")
#     answer = res["result"]
#     answer = answer.replace(".", ".\n")
#     sources = res["source_documents"]

#     if sources:
#         answer += f"\nSources: " + str(str(sources))
#     else:
#         answer += f"\nNo Sources found"

#     await cl.Message(content=answer).send()
