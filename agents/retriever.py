from graph.state import ResearchState
from tools.vector_search import vectorSearch
from tools.reranker import reranker
from config.config import config
from groq import Groq
from loguru import logger
from dotenv import load_dotenv
import os
load_dotenv()


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def retriever(state: ResearchState):
    logger.info("Retriever Node Running")
    query = state.get("query")
    llm_model = config.llm_model

    
    retrieved_nodes = vectorSearch(query=query)

    #reranked_nodes = reranker(retrieved_nodes=retrieved_nodes)

    node_texts = "\n\n".join([node.get_content() for node in retrieved_nodes])
    
    system_prompt = f"""You are a retriever agent. Analyze this \
        query and summarize what needs to be researched.
        """
    user_prompt = f"""f"Query: {query}\n\n retrieved results: {node_texts}\n\n \
        Provide a detailed research summary"""
    
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
        logger.error(f"Retriever LLM call failed: {e}")
        return {"retrieved_results": "Retrieve Failed"}
    
    retrieved_results = response.choices[0].message.content
    logger.info("Retriever Node Complete")

    return {"retrieved_results": retrieved_results}