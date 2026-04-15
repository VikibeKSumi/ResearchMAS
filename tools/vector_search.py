from config.config import config
from llama_index.core import StorageContext, load_index_from_storage
from loguru import logger



def vectorSearch(query: str):

    vectordb_path = config.vectordb_path

    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=vectordb_path
        )
    except Exception as e:
        logger.error(f"Vector Database does not exist")
        return "No Vector DB found"

    loaded_index = load_index_from_storage(
        storage_context=storage_context
    )
        
    retriever = loaded_index.as_retriever(
        similarity_top_k=10
    )
    
    retrieved_nodes = retriever.retrieve(
        query=query
    )

    return retrieved_nodes
    