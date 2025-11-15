"""
LLM modules for easy import across the project.
"""

from .ollama_model import get_ollama_llm, default_ollama_llm
from .gemini import get_gemini_llm, default_gemini_llm

__all__ = [
    "get_ollama_llm",
    "default_ollama_llm",
    "get_gemini_llm",
    "default_gemini_llm",
]

