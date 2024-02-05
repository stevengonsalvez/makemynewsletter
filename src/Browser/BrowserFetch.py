from Safari import SafariBrowser
from Chrome import ChromeBrowser
import requests

class BrowserContentFetcher:
    def __init__(self, browser_type):
        self.browser = self._select_browser(browser_type)

    def _select_browser(self, browser_type):
        if browser_type == 'safari':
            return SafariBrowser()
        elif browser_type == 'chrome':
            return ChromeBrowser()
        elif browser_type == 'firefox':
            # return FirefoxBrowser() # Assume this is implemented
            pass
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
    def _process_content(self, url):
        """Fetches and converts content to Markdown."""
        print(f"Processing {url}")
        html_content = self.browser.download_content(url)
        if html_content:
            # Convert the HTML content to Markdown
            markdown_content = self.browser.convert_to_markdown(html_content)
            return markdown_content
        else:
            print(f"Failed to download content for {url}")
            return None

    def fetch_and_save_all_content(self, output_folder='output_markdown'):
        """Fetches content and saves it."""
        urls = self.browser.get_urls()
        for url in urls:
            content = self._process_content(url)
            if content:
                filename = self._generate_filename(url)
                self.browser.save_content(content, filename, output_folder)
                print(f"Saved {filename} in {output_folder}")

    def fetch_and_return_all_content(self):
        """Fetches content and returns it."""
        urls = self.browser.get_urls()
        content_list = []
        for url in urls:
            content = self._process_content(url)
            if content:
                content_list.append(content)
        return content_list
    

    def _generate_filename(self, url):
        """Utility method to generate a filename based on the URL."""
        filename = url.split('//')[-1].replace('/', '_').replace('?', '_')[:50] + '.md'  # Simplify the URL for filename
        return filename
    


if __name__ == "__main__":
    fetcher = BrowserContentFetcher('safari')
    test = fetcher.fetch_and_return_all_content()
    print(test)