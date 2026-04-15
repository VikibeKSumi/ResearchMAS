import os
from tavily import TavilyClient
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=api_key, timeout=60)

def web_search(query: str="") -> str:
    logger.info("Web Search Tool Running")
    response = client.search(query=query, max_results=2)
    search_contents = response.get("results", [])
    web_search_result = "\n\n".join(r.get("content","") for r in search_contents)
    logger.info("Web Search Tool Completed")
    return {"web_search_result": web_search_result}