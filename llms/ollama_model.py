from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()


def get_ollama_llm(model_name: str = "llama3.1:8b"):
    """
    Get an Ollama LLM instance.
    
    Args:
        model_name: Name of the Ollama model to use. Defaults to "llama3.1:8b"
    
    Returns:
        ChatOllama instance configured with the specified model
    """
    return ChatOllama(model=model_name)


# Default instance for easy import
default_ollama_llm = get_ollama_llm()

