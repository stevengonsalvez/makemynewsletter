import subprocess
import html2text
import requests
import os
from ScriptingBridge import SBApplication


from abc import ABC, abstractmethod

class IBrowserInterface(ABC):
    @abstractmethod
    def get_urls(self):
        pass

    @abstractmethod
    def download_content(self, url):
        pass

    @abstractmethod
    def convert_to_markdown(self, html_content):
        pass

    @abstractmethod
    def save_content(self, markdown_content, filename):
        pass


class ChromeBrowser(IBrowserInterface):
    def get_urls(self):
        script = """
        osascript -e '
        set urlList to ""
        tell application "Google Chrome"
            set windowCount to count every window
            repeat with i from 1 to windowCount
                set tabCount to count every tab of window i
                repeat with j from 1 to tabCount
                    set urlList to urlList & URL of tab j of window i & "\\n"
                end repeat
            end repeat
        end tell
        return urlList
        '
        """
        output = subprocess.check_output(script, shell=True, text=True)
        return output.strip().split('\n')

    def download_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None

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