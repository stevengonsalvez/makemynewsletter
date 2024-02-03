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
