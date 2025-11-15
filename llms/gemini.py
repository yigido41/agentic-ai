from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_gemini_llm(model: str = "gemini-2.5-flash"):
    """
    Get a Gemini LLM instance.
    
    Args:
        model: Name of the Gemini model to use. Defaults to "gemini-2.5-flash"
    
    Returns:
        ChatGoogleGenerativeAI instance configured with the specified model
    """
    return ChatGoogleGenerativeAI(model=model)


# Default instance for easy import
default_gemini_llm = get_gemini_llm()
