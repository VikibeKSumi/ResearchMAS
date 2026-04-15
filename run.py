from graph.graph import graph
from loguru import logger

if __name__ == "__main__":
    
    logger.info("GRAPH EXECUTION STARTED")
    query = "what is an epstein file? and what are the key outcomes of it?"
    agent = graph(query=query)
    agent.run_graph()
    logger.info("GRAPH EXECUTION SUCCESSFUL")