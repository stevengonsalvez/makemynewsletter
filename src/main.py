import sys, os

folder_llm_path = os.path.abspath('./src/LLM')  # Adjust this path as necessary

# Only append if not already in sys.path
if folder_llm_path not in sys.path:
    sys.path.append(folder_llm_path)
from LLM import Summarize

# from LLM import summarize


# self.fetcher = BrowserContentFetcher('safari')