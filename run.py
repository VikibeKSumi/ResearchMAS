from graph.graph import graph
from loguru import logger
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ResearchMAS - Multi-Agent Research System")
    parser.add_argument("query", type=str, help="Research query to run")
    args = parser.parse_args()

    logger.info("GRAPH EXECUTION STARTED")
    agent = graph(query=args.query)
    agent.run_graph()
    logger.info("GRAPH EXECUTION SUCCESSFUL")