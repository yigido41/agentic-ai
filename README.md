# AI Agents and Agentic AI

A comprehensive project demonstrating different AI agent architectures and patterns using LangChain and LangGraph. This repository contains implementations of ReAct agents, reflection-based agents, and modular LLM integrations.

## 📁 Project Structure

```
ai_agents/
├── agent-1/                    # ReAct Agent Implementation
│   ├── re-act-agent.py        # Main ReAct agent with tools
│   └── llm-check.py           # LLM testing script
├── agent-2/                    # Reflection Agent Implementation
│   ├── reflection-agent.py    # LangGraph-based reflection agent
│   └── chain.py               # Prompt chains for generation and reflection
├── llms/                       # Modular LLM Integration
│   ├── __init__.py            # Package exports
│   ├── gemini.py              # Google Gemini LLM integration
│   └── ollama_model.py        # Ollama LLM integration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
# Windows PowerShell
.\venv\Scripts\Activate

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API Key (required for Gemini models)
GOOGLE_API_KEY=your_gemini_api_key_here

# Tavily Search API Key (optional, for search functionality)
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run Agents

```bash
# Run ReAct Agent
python agent-1/re-act-agent.py

# Run Reflection Agent
python agent-2/reflection-agent.py
```

---

## 📚 Concepts and Techniques

### What are AI Agents?

**AI Agents** are autonomous systems that can perceive their environment, make decisions, and take actions to achieve specific goals. Unlike simple chatbots, agents can:
- Use tools and external APIs
- Maintain state and memory
- Make multi-step decisions
- Iterate and improve their outputs

### Agent Architectures in This Project

---

## 🤖 Agent-1: ReAct Agent

**Location:** `agent-1/re-act-agent.py`

### What is ReAct?

**ReAct** (Reasoning + Acting) is an agent framework that combines:
- **Reasoning**: The agent thinks through problems step-by-step
- **Acting**: The agent uses tools to gather information or perform actions
- **Observation**: The agent observes results and adjusts its approach

### Architecture Flow

```
User Query
    ↓
Agent Reasoning (Thought)
    ↓
Tool Selection (Action)
    ↓
Tool Execution (Observation)
    ↓
Final Answer or Next Thought
```

### Key Components

#### 1. **LLM (Large Language Model)**
- **Gemini 2.5 Flash**: Google's fast, efficient language model
- **Ollama (llama3.1:8b)**: Local LLM option for privacy-sensitive tasks

#### 2. **Tools**
Tools are functions the agent can call to interact with the world:

- **`get_current_time`**: Custom tool that returns the current date and time
  - Purpose: Allows the agent to answer time-sensitive questions
  - Implementation: Uses Python's `datetime` module

- **`TavilySearchResults`**: Web search tool (optional)
  - Purpose: Enables the agent to search the internet for real-time information
  - Requires: `TAVILY_API_KEY` in `.env` file

#### 3. **Agent Type: Zero-Shot ReAct**
- **Zero-Shot**: The agent doesn't need examples to understand tasks
- **ReAct**: Follows the Reasoning → Action → Observation loop

### Code Flow Explanation

```python
# 1. Initialize LLM
gemini_llm = get_gemini_llm()

# 2. Define Tools
tools = [current_time_tool, search_tool]

# 3. Create Agent
agent = initialize_agent(
    tools, 
    gemini_llm, 
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

# 4. Invoke Agent
agent.invoke({"input": "Your question here"})
```

### Example Usage

```python
agent.invoke({
    "input": "When did the Bihar election result 2025 was announced and who won the election? How many days ago was it?"
})
```

**What happens:**
1. Agent **thinks**: "I need to find information about Bihar election results"
2. Agent **acts**: Uses search tool to find election information
3. Agent **observes**: Gets search results
4. Agent **thinks**: "I need to calculate days ago from current time"
5. Agent **acts**: Uses `get_current_time` tool
6. Agent **observes**: Gets current time
7. Agent **thinks**: "I can now calculate the difference"
8. Agent **answers**: Provides complete answer with all information

### Key Features

- **Error Handling**: `handle_parsing_errors=True` allows the agent to recover from format errors
- **Verbose Mode**: Shows the agent's reasoning process step-by-step
- **Tool Flexibility**: Works with or without optional tools (graceful degradation)

---

## 🔄 Agent-2: Reflection Agent

**Location:** `agent-2/reflection-agent.py`

### What is a Reflection Agent?

A **Reflection Agent** uses an iterative improvement pattern:
1. **Generate** content
2. **Reflect** on the quality
3. **Refine** based on feedback
4. Repeat until satisfied

This is similar to how humans write: draft → review → revise → repeat.

### Architecture: LangGraph StateGraph

**LangGraph** is a framework for building stateful, multi-actor applications with LLMs.

#### StateGraph Concepts

- **State**: The current data/context (messages in this case)
- **Nodes**: Functions that process state
- **Edges**: Connections between nodes (can be conditional)
- **Graph**: The overall flow structure

### Graph Flow

```
START
  ↓
GENERATE (Create content)
  ↓
Should Continue? (Check message count)
  ├─→ END (if messages > 4)
  └─→ REFLECT (if messages ≤ 4)
      ↓
      GENERATE (Refine based on feedback)
      ↓
      (Loop continues...)
```

### Key Components

#### 1. **Generation Chain** (`chain.py`)
```python
generation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an Instagram techie influencer..."),
    MessagesPlaceholder(variable_name="messages"),
])
generation_chain = generation_prompt | llm
```

- **Purpose**: Generates Instagram post content
- **Prompt Engineering**: System message defines the agent's role and behavior
- **Chain Composition**: Uses LangChain's pipe operator (`|`) to combine prompt and LLM

#### 2. **Reflection Chain** (`chain.py`)
```python
reflection_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a viral Instagram influencer grading a post..."),
    MessagesPlaceholder(variable_name="messages"),
])
reflection_chain = reflection_prompt | llm
```

- **Purpose**: Critiques and provides feedback on generated content
- **Role**: Acts as a quality reviewer
- **Output**: Recommendations for improvement

#### 3. **State Management**
```python
class GraphState(TypedDict):
    messages: List[BaseMessage]
```

- **TypedDict**: Provides type safety for state structure
- **Messages**: Stores conversation history (user input, generations, reflections)

#### 4. **Node Functions**

**Generate Node:**
```python
def generate_node(state: GraphState):
    result = generation_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [result]}
```
- Takes current messages
- Generates new content
- Appends to message history

**Reflect Node:**
```python
def reflect_node(state: GraphState):
    response = reflection_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [HumanMessage(content=response.content)]}
```
- Reviews all messages
- Provides critique
- Adds critique as a new message

#### 5. **Conditional Logic**
```python
def should_continue(state: GraphState):
    if len(state["messages"]) > 4:
        return END
    return REFLECT
```
- **Purpose**: Prevents infinite loops
- **Logic**: Stops after 4 iterations
- **Conditional Edge**: Routes based on state

### Example Usage

```python
response = app.invoke({
    "messages": [HumanMessage(content="AI Agents taking over content creation")]
})
```

**What happens:**
1. **Iteration 1**: Generates initial Instagram post
2. **Reflection 1**: Critiques the post (length, style, virality)
3. **Iteration 2**: Generates improved version based on feedback
4. **Reflection 2**: Provides more specific recommendations
5. **Iteration 3**: Further refinement
6. **Final Output**: High-quality, refined content

### Key Concepts

- **Iterative Refinement**: Each cycle improves the output
- **Self-Critique**: The agent evaluates its own work
- **State Persistence**: Messages accumulate, building context
- **Graph-Based Flow**: Visual, declarative workflow definition

---

## 🧠 LLMs Module

**Location:** `llms/`

### Purpose

Centralized, reusable LLM integration for easy model switching across the project.

### Architecture

#### 1. **Gemini Integration** (`llms/gemini.py`)

```python
def get_gemini_llm(model: str = "gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(model=model)
```

- **Provider**: Google AI
- **Default Model**: `gemini-2.5-flash` (fast, efficient)
- **Use Cases**: Production applications, real-time responses
- **Requirements**: `GOOGLE_API_KEY` in `.env`

#### 2. **Ollama Integration** (`llms/ollama_model.py`)

```python
def get_ollama_llm(model_name: str = "llama3.1:8b"):
    return ChatOllama(model=model_name)
```

- **Provider**: Local (self-hosted)
- **Default Model**: `llama3.1:8b` (Meta's Llama 3.1)
- **Use Cases**: Privacy-sensitive tasks, offline operation
- **Requirements**: Ollama installed locally with models pulled

### Usage Pattern

```python
from llms import get_gemini_llm, get_ollama_llm

# Use Gemini
llm = get_gemini_llm()

# Use Ollama
llm = get_ollama_llm()

# Use custom model
llm = get_gemini_llm("gemini-pro")
llm = get_ollama_llm("mistral:latest")
```

### Benefits

- **Modularity**: Easy to swap models
- **Consistency**: Same interface across models
- **Environment Management**: Automatic `.env` loading
- **Default Instances**: Pre-configured models available

---

## 🔧 Technical Concepts

### 1. **Prompt Engineering**

**Definition**: The art of crafting inputs to get desired outputs from LLMs.

**In This Project:**
- System messages define agent roles
- MessagesPlaceholder allows dynamic conversation history
- Chain composition links prompts to LLMs

### 2. **Chain Composition**

**Definition**: Combining multiple components (prompts, LLMs, tools) into reusable pipelines.

**Syntax:**
```python
chain = prompt | llm | output_parser
```

**Benefits:**
- Reusable components
- Clear data flow
- Easy to modify and extend

### 3. **State Management**

**Definition**: Maintaining context and data across agent interactions.

**In LangGraph:**
- TypedDict defines state structure
- Nodes read and update state
- State persists across graph execution

### 4. **Tool Integration**

**Definition**: Functions that agents can call to interact with external systems.

**Types:**
- **Custom Tools**: Python functions wrapped for agent use
- **External Tools**: APIs and services (Tavily, etc.)

**Requirements:**
- Single string input (for compatibility)
- Clear descriptions (for agent selection)
- Proper error handling

### 5. **Error Handling**

**Strategies Used:**
- `handle_parsing_errors=True`: Recovers from format errors
- Try-except blocks: Graceful tool failures
- Conditional tool loading: Works without optional dependencies

---

## 📦 Dependencies

### Core Libraries

- **langchain**: Framework for building LLM applications
- **langchain-google-genai**: Google Gemini integration
- **langchain-ollama**: Ollama integration
- **langchain-community**: Community tools and integrations
- **langgraph**: Graph-based agent framework

### Supporting Libraries

- **python-dotenv**: Environment variable management
- **langchain-tavily**: Tavily search integration (optional)

### Development Tools

- **mlflow**: Experiment tracking
- **dvc**: Data version control
- **langsmith**: To trace LLM calls and langchain chain calls/execution also to evaluate the ai agent/apps

---

## 🎯 Use Cases

### ReAct Agent (Agent-1)
- **Information Retrieval**: Answer questions requiring real-time data
- **Multi-Step Reasoning**: Complex queries needing multiple tools
- **Time-Sensitive Queries**: Questions about dates, events, timelines

### Reflection Agent (Agent-2)
- **Content Generation**: High-quality, refined content creation
- **Iterative Improvement**: Tasks requiring multiple refinement cycles
- **Quality Assurance**: Self-reviewing and improving outputs

---


## 📖 Further Reading

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama Documentation](https://ollama.ai/docs)

---



## 🎓 Learning Path

1. **Start with Agent-1**: Understand basic ReAct pattern
2. **Explore Tools**: Modify and add custom tools
3. **Study Agent-2**: Learn graph-based workflows
4. **Experiment**: Try different models and prompts
5. **Build**: Create your own agent architectures

---

**Happy Agent Building! 🚀**
