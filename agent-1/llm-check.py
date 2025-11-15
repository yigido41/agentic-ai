import sys
from pathlib import Path

# Add parent directory to Python path to import llms module
sys.path.insert(0, str(Path(__file__).parent.parent))

from llms import get_gemini_llm, get_ollama_llm

# Using Gemini model (default: gemini-2.5-flash)
gemini_llm = get_gemini_llm()
gemini_answer = gemini_llm.invoke("What is the capital of France?")
print("Gemini Response:")
print(gemini_answer)

# Using Ollama model (default: llama3.1:8b)
ollama_llm = get_ollama_llm()
ollama_answer = ollama_llm.invoke("What is the capital of France?")
print("\nOllama Response:")
print(ollama_answer)

# You can also use custom models:
# custom_gemini = get_gemini_llm("gemini-pro")
# custom_ollama = get_ollama_llm("mistral:latest")

