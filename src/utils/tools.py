from langchain.text_splitter import MarkdownTextSplitter


def markdown_chunker(content: str):

    markdown_splitter = MarkdownTextSplitter (chunk_size=2000, chunk_overlap=0)
    docs = markdown_splitter.create_documents(content)
    # print(docs)
    return docs