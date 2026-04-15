from groq import Groq
from dotenv import load_dotenv
import os
from graph.state import ResearchState
from loguru import logger
from config.config import config


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def critic(state: ResearchState):
    
    logger.info("Critic Node Running")
    revision_count = state.get("revision_count", 0)
    llm_model = config.llm
    writer_result = state.get("writer_result","")
    revision_needed = False
    research_needed = False

    if revision_count >= 2:
        logger.info("Critic Node Complete")
        return {"critic_result": "FINISH",
                "revision_needed": revision_needed,
                "research_needed": research_needed,
                "revision_count": 1}
   
   
    prompt = f"check the given content {writer_result} and give only one word output of these Three\
        -RESEARCH\
        -REVISION\
        -FINISH\
        return them in upper case."
    
    messages = [
        {"role": "system", "content": """You are a strict critic. Review the writing and return exactly one word:
            - REVISION if the content is poorly structured or unclear but has enough information
            - RESEARCH if critical facts are completely missing or the content is too thin to work with
            - FINISH if the content is reasonably complete, coherent, and addresses the query
            """},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
    except Exception as e:
        logger.error(f"Critic LLM call failed: {e}")
        return {"critic_result": "Critic failed",
            "revision_needed": False, 
            "research_needed": False,
            "revision_count": 1}

    critic_result = response.choices[0].message.content

    if critic_result == 'RESEARCH':
        research_needed = True
    elif critic_result == 'REVISION':
        revision_needed = True

    logger.info("Critic Node Complete")

    return {"critic_result": critic_result,
            "revision_needed": revision_needed, 
            "research_needed": research_needed,
            "revision_count": 1}
    