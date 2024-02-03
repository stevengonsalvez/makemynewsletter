import os
import requests
import html2text
from ScriptingBridge import SBApplication
from IBrowserInterface import IBrowserInterface

class SafariBrowser(IBrowserInterface):
    def get_urls(self):
        safari = SBApplication.applicationWithBundleIdentifier_("com.apple.Safari")
        return [tab.URL() for window in safari.windows() for tab in window.tabs()]

    def download_content(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def convert_to_markdown(self, html_content):
        h = html2text.HTML2Text()
        h.ignore_links = False
        return h.handle(html_content)

    def save_content(self, markdown_content, filename, output_folder='output_markdown'):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filepath = os.path.join(output_folder, filename)
        with open(filepath, 'w') as md_file:
            md_file.write(markdown_content)