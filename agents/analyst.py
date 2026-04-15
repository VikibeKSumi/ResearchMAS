from graph.state import ResearchState
from groq import Groq
import os
from dotenv import load_dotenv
from loguru import logger
from config.config import config


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def analyst(state: ResearchState):
    logger.info("Analyst Node Running")
    researcher_result = state.get("researcher_result", "")
    llm_model = config.llm

    messages = [
        {"role": "system", "content": "you are an analyst, Analyse the research summary and extract structured insights — key facts, gaps, conclusions"},
        {"role": "user", "content": f"summarize {researcher_result}"}
    ]

    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
    except Exception as e:
        logger.error(f"Analyst LLM call failed: {e}")
        return {"analyst_result": "Analysis failed"}
    
    analyst_result = response.choices[0].message.content
    logger.info("Analyst Node Complete")
    return {"analyst_result": analyst_result}