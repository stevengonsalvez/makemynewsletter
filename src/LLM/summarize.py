import re
import sys, os
# from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from unstructured.cleaners.core import remove_punctuation,clean,clean_extra_whitespace
from langchain.text_splitter import MarkdownTextSplitter
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from Schema import BlogSummary


# Assuming you're running this from inside Folder_B or its parent
folder_a_path = os.path.abspath('./src/Browser')  # Adjust this path as necessary

# Only append if not already in sys.path
if folder_a_path not in sys.path:
    sys.path.append(folder_a_path)
from BrowserFetch import BrowserContentFetcher

def is_valid_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(re.match(pattern, url))

def generate_document(url):
    "Given an URL, return a langchain Document to further processing."
    loader = UnstructuredURLLoader(urls=[url],
    mode="elements",
    post_processors=[clean,remove_punctuation,clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [e for e in elements if e.metadata['category']=="NarrativeText"]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source":url})

def summarize_document(url,model_name):
    "Given an URL return the summary from OpenAI model"
    llm = OpenAI(model_name='gpt-3.5-turbo-0613',temperature=0,openai_api_key=openai_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    tmp_doc = generate_document(url)
    summary = chain.run([tmp_doc])
    return clean_extra_whitespace(summary)


def summarize_markdown_content(markdown: str):
    "Given this Markdown content that is extacted from a webpage"

    pydantic_parser = PydanticOutputParser(pydantic_object=BlogSummary)
    format_instructions = pydantic_parser.get_format_instructions()
    # print(format_instructions)

    md_format_instructions="""
        The output should be formatted as a markdown with proper line endings "\n" and it should conform to the following structure
        ```
        # Title
        ## Quick Summary
        ### Key Points
        ## Hyperlinks
    """


    docs = markdown_chunker(markdown)
    # map_prompt = """
    #     Write a concise summary of the following:
    #     "{text}"
    #     CONCISE SUMMARY:
    #     """
    # map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"], 

    bullet_prompt = """
    Write a summary of the following text delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the text. Do not make it extremely concise , it should convey the core essence of the blog
    Append the source_url of it at the beginning of the summary. The document will contain the text "source_url"
    Create an appendix in the summary to contain all hyperlinks present in the text. Do not summarise the hyperlinks, need all hyperlinks to be present
    ```{text}```
    {md_format_instructions}
    """
    bullet_prompt_template = PromptTemplate(template=bullet_prompt, input_variables=["text"],
                                            partial_variables={"md_format_instructions": md_format_instructions}
                                        )
    # combine_prompt = """
    # Write a summary of the following text delimited by triple backquotes.
    # Return your response in bullet points which covers the key points of the text.
    # Have a reference of the source url . Preserve all links to images and external http and https links at the appendix. Capture the author name
    # ```{text}```
    # {format_instructions}
    # """
    
    # combine_prompt_template = PromptTemplate(template=bullet_prompt, input_variables=["text"], 
    #                                         partial_variables={"format_instructions": format_instructions}
    #                                          )
    # summary_chain = LLMChain(llm=llm,
    #                                  chain_type='map_reduce',
    #                                  map_prompt=map_prompt_template,
    #                                 #  combine_prompt=combine_prompt_template,
    #                                  #verbose=True
    #                                 )

    custom_summary_chain = LLMChain(llm=llm, prompt=bullet_prompt_template)
    output = custom_summary_chain.run(docs)
    return output
 


def markdown_chunker(content: str):

    markdown_splitter = MarkdownTextSplitter (chunk_size=2000, chunk_overlap=0)
    docs = markdown_splitter.create_documents(content)
    return docs


# API Keys for OPENAI
LLM_KEY=os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0, openai_api_key=LLM_KEY)

fetcher = BrowserContentFetcher('safari')
md = fetcher.fetch_and_return_all_content()
# print(len(md))
print(summarize_markdown_content(md))


