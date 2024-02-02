import os
import requests
import html2text
from Foundation import *
from ScriptingBridge import *

# Define a function to get all URLs from open Safari tabs
def get_safari_urls():
    safari = SBApplication.applicationWithBundleIdentifier_("com.apple.Safari")
    urls = []
    for window in safari.windows():
        for tab in window.tabs():
            urls.append(tab.URL())
    return urls

# Define a function to download webpage content
def download_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

# Define a function to convert HTML to Markdown
def convert_html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html_content)

# Define a function to save content to a Markdown file
def save_markdown_file(markdown_content, filename, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'w') as md_file:
        md_file.write(markdown_content)

# Main function to orchestrate the scraping and conversion process
def main(output_folder='output_markdown'):
    urls = get_safari_urls()
    for url in urls:
        print(f"Processing {url}")
        html_content = download_webpage_content(url)
        if html_content:
            markdown_content = convert_html_to_markdown(html_content)
            # Simplify the URL to create a filename
            filename = url.split('//')[-1].replace('/', '_').replace('?', '_')[:50] + '.md'  # Limit filename length
            save_markdown_file(markdown_content, filename, output_folder)
            print(f"Saved {filename} in {output_folder}")

if __name__ == "__main__":
    main()
