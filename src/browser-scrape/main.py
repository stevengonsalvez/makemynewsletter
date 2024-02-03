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

    def fetch_and_save_all_content(self):
        urls = self.browser.get_urls()
        for url in urls:
            print(f"Processing {url}")
            html_content = self.browser.download_content(url)
            if html_content:  # Ensure html_content is not None
                markdown_content = self.browser.convert_to_markdown(html_content)
                # Simplify the URL to create a filename
                filename = url.split('//')[-1].replace('/', '_').replace('?', '_')[:50] + '.md'  # Limit filename length
                self.browser.save_content(markdown_content, filename, 'output_markdown')
                print(f"Saved {filename} in output_markdown")
            else:
                print(f"Failed to download or convert content for {url}")

    def _generate_filename_from_url(self, url):
        # Simplify the URL to create a filename
        filename = url.split('//')[-1].replace('/', '_').replace('?', '_')[:50] + '.md'  # Limit filename length
        return filename
    


if __name__ == "__main__":
    fetcher = BrowserContentFetcher('chrome')
    fetcher.fetch_and_save_all_content()