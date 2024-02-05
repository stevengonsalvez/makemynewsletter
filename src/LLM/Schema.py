from pydantic import BaseModel, HttpUrl, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser


class BlogSummary(BaseModel):
    """
    Represents a summary of a blog post.

    Attributes:
        url (HttpUrl): The URL of the blog post.
        author (str): The author of the blog post.
        quick_summary (str): A brief summary of the blog post.
        content (str): The full content of the blog post.
        image_links (List[HttpUrl]): A list of URLs for images in the blog post.
        references (List[HttpUrl]): A list of URLs for references mentioned in the blog post.
    """
    url: HttpUrl = Field(..., description="The URL of the blog post.")
    author: str = Field(..., description="The author of the blog post.")
    quick_summary: str = Field(..., description="A brief summary of the blog post.")
    content: str = Field(..., description="The full content of the blog post.")
    image_links: List[HttpUrl] = Field(..., description="A list of URLs for images in the blog post.")
    references: List[HttpUrl] = Field(..., description="A list of URLs for all links mentioned in the blog post.")
