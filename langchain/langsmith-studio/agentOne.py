from langchain.agents import create_agent

from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)


agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
)