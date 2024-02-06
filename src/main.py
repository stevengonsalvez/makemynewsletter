import sys, os

folder_llm_path = os.path.abspath('./src/LLM')  # Adjust this path as necessary
folder_browser_path = os.path.abspath('./src/Browser')
folder_util_path = os.path.abspath('./src/utils')

# Only append if not already in sys.path
if folder_llm_path not in sys.path:
    sys.path.append(folder_llm_path)
if folder_browser_path not in sys.path:
    sys.path.append(folder_browser_path)
if folder_util_path not in sys.path:
    sys.path.append(folder_util_path)

from LLM import summarize, storage
from Browser import browserfetch
from utils import tools

# fetcher = browserfetch.BrowserContentFetcher('safari')
# content_list = fetcher.fetch_and_return_all_content()
# summarizer = summarize.Summarizer()
storage_obj = storage.Embedder()

# for item in content_list:

#     # Converting back to a list of one as markdownchunker needs a list
#     i_arr = [item]
#     summary = summarizer.summarize_markdown_content(i_arr)
#     s_arr = tools.generate_tokens(summary)
#     storage_obj.embed_document_chroma(s_arr)

print(storage_obj.get_documents())