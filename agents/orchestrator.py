from graph.state import ResearchState
from config.config import config
from loguru import logger
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def orchestrator(state: ResearchState):
    logger.info("Orchestrator Node Running")

    query = state.get("query","")
    llm_model = config.llm
    
    system_prompt = """You are a query re-writer. You take a given query and\
    rewrite it so it can be best understood by LLM
    """

    user_prompt = f"""analyze the query and clarify what specifically\
        needs to be researched. Based on that rewrite the query '{query}'.\
        Refining it in a way that is concise, and adquate for an LLM.\
        return ONLY the rewritten query. No explanation. Maximum 200 characters.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )

    except Exception as e:
        logger.error(f"Orchestrator LLM call failed: {e}")
        return {"query": "Query Rewriting Failed"}

    refined_query = response.choices[0].message.content
    logger.info("Orchestrator Node Complete")
    return {"query": refined_query}