import os

llm = dict(
    type='openai',
    model='gpt-3.5-turbo-0613',
    key=os.environ.get('OPENAI_API_KEY'),
    embedding_model='text-embedding-3-large'
)

vectordb = dict(
    type='chroma',
    persist_directory='output_db',
    collection_name='langchain'
)

codebase_vectordb = dict(
    type='chroma',
    persist_directory='output_db',
    collection_name='codebase'
    # collection_name='codebase_' + str(uuid.uuid4())
)

codebase_llm = dict(
    type='openai',
    model='gpt-4-1106-preview',
    key=os.environ.get('OPENAI_API_KEY'),
    embedding_model='text-embedding-3-large'
)