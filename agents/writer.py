from graph.state import ResearchState
import os
from groq import Groq
from loguru import logger
from config.config import config


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def writer(state: ResearchState):
    logger.info("Writer Node Running")

    analyst_result = state.get("analyst_result", "")
    llm_model = config.llm_model


    prompt = f"use {analyst_result} and turn it into a writing.\
            provide clear section: \
            - Summary\
            -Key findings\
            - conclusion\
    "
    messages = [
        {"role": "system", "content": "you are a professional writer that reads unstructured writings and turn it into a well-structured report"},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
    except Exception as e:
        logger.error(f"Writer LLM call failed: {e}")
        return {"writer_result": "Writing Failed"}

    writer_result = response.choices[0].message.content
    logger.info("Writer Node Complete")
    return {"writer_result": writer_result}