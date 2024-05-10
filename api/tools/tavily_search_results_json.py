from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults


def load_tavily_search_results_json_tool():
    tavily_search_results = TavilySearchResults(max_results=1)
    return Tool.from_function(
        name=tavily_search_results.name,
        func=tavily_search_results,
        description=tavily_search_results.description,
    )
