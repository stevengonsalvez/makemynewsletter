import sys, os

folder_llm_path = os.path.abspath('./src/LLM')  # Adjust this path as necessary
folder_browser_path = os.path.abspath('./src/Browser')

# Only append if not already in sys.path
if folder_llm_path not in sys.path:
    sys.path.append(folder_llm_path)
if folder_browser_path not in sys.path:
    sys.path.append(folder_browser_path)
from LLM import summarize
from Browser import browserfetch

fetcher = browserfetch.BrowserContentFetcher('safari')
content_list = fetcher.fetch_and_return_all_content()
summarizer = summarize.Summarizer()

for item in content_list:

    # Converting back to a list of one as markdownchunker needs a list
    i_arr = []
    i_arr.append(item)
    summary = summarizer.summarize_markdown_content(i_arr)
    print (summary)