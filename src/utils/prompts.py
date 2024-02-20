from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain import hub

# Loads the latest version
def get_codeqa_prompt_hub():
    prompt = hub.pull("rlm/rag-prompt", api_url="https://api.hub.langchain.com")
    return prompt


def get_codeqa_prompt():
    prompt = PromptTemplate.from_template(
        """
        ### CodeQA
        Given the following code snippet and question, answer the question.
        ```
        {example}
        ```
        {question}
        """
    )
    return prompt


