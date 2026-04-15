import os
from groq import Groq
from loguru import logger
from dotenv import load_dotenv

from tools.web_search import web_search
from graph.state import ResearchState
from config.config import config

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def researcher(state: ResearchState) -> dict:
    logger.info("Researcher Node Running")
    query = state.get('query')
    llm_model = config.llm
    
    try:
        web_search_result = web_search(query=query)
    except Exception as e:
        logger.error(f"Web Search Failed: {e}")
        return {"researcher_result": "Websearch Failed"}
    
    messages = [
        {"role": "system", "content": "You are a research agent. Analyze this query and summarize what needs to be researched."},
        {"role": "user", "content": f"Query: {query}\n\nSearch results: {web_search_result}\n\nProvide a detailed research summary."}
    ]

    try:
        final_response = client.chat.completions.create(
                model=llm_model,
                messages=messages
            )
    except Exception as e:
        logger.error(f"Researcher LLM call failed: {e}")
        return {"researcher_result": "Research Failed", "web_search_result":web_search_result}
    

    researcher_result = final_response.choices[0].message.content
    logger.info("Researcher Node Completed")
    return {"researcher_result": researcher_result, "web_search_result": web_search_result}
