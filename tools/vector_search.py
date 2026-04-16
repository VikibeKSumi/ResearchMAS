from config.config import config
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from loguru import logger


def vectorSearch(query: str):
    logger.info("Vector Search Tool Running")
    Settings.embed_model = HuggingFaceEmbedding(
        model_name = config.bi_encoder
    )

    vectordb_path = config.vectordb_path

    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=vectordb_path
        )
    except Exception as e:
        logger.error(f"Vector Database does not exist: {e}")
        return None

    loaded_index = load_index_from_storage(
        storage_context=storage_context
    )
        
    retriever = loaded_index.as_retriever(
        similarity_top_k=10
    )
    
    retrieved_nodes = retriever.retrieve(query)
    logger.info("Vector Search Tool Complete")
    return retrieved_nodes
    