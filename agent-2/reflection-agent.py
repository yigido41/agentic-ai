from typing import List, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from chain import generation_chain, reflection_chain

load_dotenv()

# Define state schema for the graph
class GraphState(TypedDict):
    messages: List[BaseMessage]

# Create StateGraph with messages key
graph = StateGraph(GraphState)

REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state: GraphState):
    """Generate content based on messages."""
    result = generation_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [result]}

def reflect_node(state: GraphState):
    """Reflect on the generated content."""
    response = reflection_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [HumanMessage(content=response.content)]}

graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)

def should_continue(state: GraphState):
    """Determine if we should continue or end."""
    if len(state["messages"]) > 4:
        return END
    return REFLECT

# Set up the graph edges
graph.add_edge(START, GENERATE)
graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

# Invoke with initial state containing messages
response = app.invoke({"messages": [HumanMessage(content="AI Agents taking over content creation")]})

print(response)