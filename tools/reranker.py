from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.schema import NodeWithScore
from config.config import config
from loguru import logger

def reranker(retrieved_nodes: NodeWithScore, query: str):
    logger.info("Reranker Tool Running")
    reranker_model = config.cross_encoder
    reranker = SentenceTransformerRerank(
        top_n = 2,
        device = "cpu",
        model=reranker_model
    )

    reranked_nodes = reranker.postprocess_nodes(
        nodes=retrieved_nodes,
        query_str=query
    )
    logger.info("Reranker Tool Complete")
    return reranked_nodes


