from mem0 import Memory
import os
from qdrant_client import QdrantClient

def get_mem0_client():
    llm_provider = os.getenv("LLM_PROVIDER", "ollama")
    llm_model = os.getenv("LLM_CHOICE", "llama3")
    embedding_model = os.getenv("EMBEDDING_MODEL_CHOICE", "nomic-embed-text")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    qdrant_client = QdrantClient(path="./qdrant_db")

    config = {
        "llm": {
            "provider": llm_provider,
            "config": {
                "model": llm_model,
                "temperature": 0.2,
                "max_tokens": 2000,
                "api_base": ollama_host
            }
        },
        "embedder": {
            "provider": llm_provider,
            "config": {
                "model": embedding_model,
                "embedding_dims": 768
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "mem0_memories",
                "client": qdrant_client
            }
        }
    }

    return Memory.from_config(config)