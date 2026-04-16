from llama_index.core import Settings, Document, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config.config import config
from loguru import logger



def ingestion():
    logger.info("INGESTION RUNNING")
    
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=config.bi_encoder
    )

    text_source = """Today's Autonomous Machines and Edge Computing systems are 
    defined by the growing needs of AI software. Fixed function devices 
    running simple convolutional neural networks for inferencing tasks like 
    object detection and classification are not able to keep up with new 
    networks that appear every day: transformers are important for natural 
    language processing for service robots; reinforcement learning can be 
    used for manufacturing robots that operate alongside humans; and autoencoders, 
    long short-term memory (LSTM), and generative adversarial networks (GAN) are needed 
    for various applications. The NVIDIA® Jetson™ platform is the ideal solution to solve 
    the needs of these complex AI systems at the edge. The platform includes Jetson 
    modules, which are small form-factor, high-performance computers, the JetPack SDK for 
    end-to-end AI pipeline acceleration, and an ecosystem with sensors, SDKs, services, and
    products to speed up development. Jetson is powered by the same AI software and cloud-native 
    workflows used across other NVIDIA platforms and delivers the performance and power-efficiency 
    customers need to build software-defined intelligent machines at the edge. For advanced 
    robotics and other autonomous machines in the fields of manufacturing, logistics, retail, 
    service, agriculture, smart city, and healthcare the Jetson platform is the ideal solution.
    The newest members of the Jetson Family, the Jetson AGX Orin series, provide a giant leap 
    forward for Robotics and Edge AI. With Jetson AGX Orin modules, customers can now deploy 
    large and complex models to solve problems such as natural language understanding, 3D 
    perception and multi-sensor fusion. In this technical brief we identify details on the new 
    architecture of the Jetson AGX Orin series and steps customers can take to leverage the full 
    capabilities of the Jetson platform."""

    doc = Document(
        text=text_source,
    )


    pipeline = IngestionPipeline()

    auto_nodes = pipeline.run(
        documents=[doc]
    )

    index = VectorStoreIndex(
        auto_nodes
    )

    vectordb_path = config.vectordb_path
    index.storage_context.persist(persist_dir=vectordb_path)
    logger.info("INGESTION COMPLETE")

if __name__ == "__main__":
    ingestion()

