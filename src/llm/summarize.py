import re
import sys
import os
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import OpenAI
from unstructured.cleaners.core import remove_punctuation, clean, clean_extra_whitespace
import warnings

from src.llm.schemas import BlogSummary
from src.utils.tools import markdown_chunker
from src.llm.llm_manager import LLMManager

warnings.filterwarnings("ignore", category=DeprecationWarning)


def generate_document(url):
    "Given an URL, return a langchain Document to further processing."
    loader = UnstructuredURLLoader(urls=[url], mode="elements",
                                   post_processors=[clean, remove_punctuation, clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [e for e in elements if e.metadata['category'] == "NarrativeText"]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source": url})


class Summarizer:
    def __init__(self, llm_manager: LLMManager=None):
        self.llm = llm_manager.get_llm()

    def summarize_document(self, url: str):
        "Given an URL return the summary from LLM model"
        chain = load_summarize_chain(self.llm, chain_type="stuff")
        tmp_doc = generate_document(url)
        summary = chain.run([tmp_doc])
        return clean_extra_whitespace(summary)

    def summarize_markdown_content(self, markdown: list):
        "Given this Markdown content that is extacted from a webpage"
        pydantic_parser = PydanticOutputParser(pydantic_object=BlogSummary)
        format_instructions = pydantic_parser.get_format_instructions()

        md_format_instructions = """
            The output should be formatted as a markdown with proper line endings "\n" and it should conform to the following structure
            ```
            # Title
            ## Quick Summary
            ### Key Points
            ## Hyperlinks
        """

        docs = markdown_chunker(markdown)

        bullet_prompt = """
        Write a summary of the following text delimited by triple backquotes.
        Return your response in bullet points which covers the key points of the text. Do not make it extremely concise, it should convey the core essence of the blog
        Append the source_url of it at the beginning of the summary. The document will contain the text "source_url"
        ```{text}```
        {md_format_instructions}
        """

        bullet_prompt_template = PromptTemplate(template=bullet_prompt, input_variables=["text"],
                                                partial_variables={"md_format_instructions": md_format_instructions}
                                            )

        custom_summary_chain = LLMChain(llm=self.llm, prompt=bullet_prompt_template)
        output = custom_summary_chain.run(docs)
        return output


