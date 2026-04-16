from graph.state import ResearchState
from groq import Groq
import os
from loguru import logger
from config.config import config



api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def analyst(state: ResearchState):
    logger.info("Analyst Node Running")
    researcher_result = state.get("researcher_result", "")
    retrieved_result = state.get("retrieved_result", "")

    llm_model = config.llm_model


    system_prompt =f"""You are an analyst. Synthesize 
        the web research and internal knowledge 
        base results into structured insights — key facts, gaps, 
        and conclusions"""
    
    user_prompt = f"""Web Research:\n{researcher_result}\n\n
        Internal Knowledge Base:\n{retrieved_result}"""
    
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
        logger.error(f"Analyst LLM call failed: {e}")
        return {"analyst_result": "Analysis failed"}
    
    analyst_result = response.choices[0].message.content
    logger.info("Analyst Node Complete")
    return {"analyst_result": analyst_result}