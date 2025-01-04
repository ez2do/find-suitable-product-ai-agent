from typing import Any, Dict, Optional
from langchain_community.utilities import BraveSearchWrapper
from crewai.tools import BaseTool
from pydantic import Field

class BraveSearchTool(BaseTool):
    """Tool for performing web searches using Brave Search."""
    
    name: str = "brave_search"
    description: str = "Useful for searching the web for current information about products, reviews, and comparisons."
    search_wrapper: BraveSearchWrapper = Field(default=None)

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.search_wrapper = BraveSearchWrapper(api_key=api_key)

    def _run(self, query: str) -> str:
        """Execute the Brave search."""
        try:
            search_results = self.search_wrapper.run(query)
            return search_results
        except Exception as e:
            return f"Error performing search: {str(e)}"
