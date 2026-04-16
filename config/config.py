import yaml
import os
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
_config_path = os.path.join(os.path.dirname(__file__), "settings.yaml")

class Config:
    def __init__(self):
        try:
            with open(_config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Config Loading Failed: {e}")
            raise SystemExit(1)   
        
        self.checkpointer_path = self.config.get("database",{}).get("checkpointer_path")
        Path(self.checkpointer_path).parent.mkdir(parents=True, exist_ok=True)
        self.vectordb_path = self.config.get("database",{}).get("vectordb_path")
        Path(self.vectordb_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.groq_api = os.getenv("GROQ_API_KEY")
        self.tavily_api = os.getenv("TAVILY_API_KEY")
        
        self.llm_model = self.config.get("models", {}).get("llm_model")
        self.bi_encoder = self.config.get("models", {}).get("bi_encoder")
        self.cross_encoder = self.config.get("models", {}).get("cross_encoder")


        try:
            self.validate()
        except ValueError as e:
            logger.error(e)
            raise SystemExit(1)    
        
    
    def validate(self):
        if not self.llm_model:
            raise ValueError("LLM model is not set in setting.yaml")
        if not self.bi_encoder:
            raise ValueError("Bi-Encoder path is not set in settings.yaml")
        if not self.cross_encoder:
            raise ValueError("Cross-Encoder path is not set in settings.yaml")
        
        if not self.checkpointer_path:
            raise ValueError("Checkpointer Database path is not set in settings.yaml")
        if not self.vectordb_path:
            raise ValueError("Vector DB path is not set in settings.yaml")
        
        if not self.groq_api:
            raise ValueError("Groq API Key is not in .env")
        if not self.tavily_api:
            raise ValueError("Tavily API Key is not in .env")
 


config = Config()