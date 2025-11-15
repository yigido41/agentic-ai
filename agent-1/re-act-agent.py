import sys
from pathlib import Path
from langchain.agents import initialize_agent
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import Tool
from dotenv import load_dotenv
import datetime
import os

# Load environment variables
load_dotenv()

# Add parent directory to Python path to import llms module
sys.path.insert(0, str(Path(__file__).parent.parent))

from llms import get_ollama_llm, get_gemini_llm

# Using Ollama model (default: llama3.1:8b)
#ollama_llm = get_ollama_llm()
gemini_llm = get_gemini_llm()

# Current time tool - Tool requires a string input parameter (even if unused)
def get_current_time(query: str = "") -> str:
    """Get the current date and time. Returns a formatted string with the current date and time.
    
    Args:
        query: Not used, but required by Tool interface. Can be empty string.
    
    Returns:
        A formatted string with the current date and time.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_time = f"The current time is {current_time}"
    return formatted_time

# Convert to LangChain tool - Tool requires single string input
current_time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description="Get the current date and time. Returns a formatted string with the current date and time. No input required."
)

# Initialize tools list
tools = [current_time_tool]

# Add Tavily search tool if API key is available
tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key:
    try:
        search_tool = TavilySearchResults(search_depth="basic", tavily_api_key=tavily_api_key)
        tools.append(search_tool)
        print("Tavily search tool loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not initialize Tavily search tool: {e}")
else:
    print("Warning: TAVILY_API_KEY not found. Tavily search tool will not be available.")
    print("To enable search, add TAVILY_API_KEY to your .env file.")

# agent - handle_parsing_errors allows the agent to retry when output parsing fails
agent = initialize_agent(
    tools, 
    gemini_llm, 
    agent="zero-shot-react-description", 
    verbose=True,
    handle_parsing_errors=True
)


#agent.invoke({"input": "When was the SpaceX's last launch and how many days ago was it?"})

agent.invoke({"input": "When did the Bihar election result 2025 was announced and who won the election?How many days ago was it?"})


