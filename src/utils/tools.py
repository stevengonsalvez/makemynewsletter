from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter


def markdown_chunker(content: str):

    markdown_splitter = MarkdownTextSplitter (chunk_size=2000, chunk_overlap=0)
    docs = markdown_splitter.create_documents(content)
    # print(docs)
    return docs


def generate_tokens(s: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_text(s)

    return text_splitter.create_documents(splits) #this should return the list of documents.