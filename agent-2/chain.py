from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import sys
from pathlib import Path

# Add parent directory to Python path to import llms module
sys.path.insert(0, str(Path(__file__).parent.parent))

from llms import get_ollama_llm, get_gemini_llm

# Using Ollama model (default: llama3.1:8b)
#llm = get_ollama_llm()
llm = get_gemini_llm()


generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a instagram techie influencer tasked with writing excellent instagram posts."
            "Generate the best instagram post possible for the given topic and hashtags for user's request."
            "If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt =  ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral instagram influencer grading a insta post. Generate critique and recommendations for the user's post."
            "Always provide detailed recommendations, including requests for length, virality, style, trend, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm