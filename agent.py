from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

from config import GROQ_API_KEY
# from tools import calculator, weather,rag

# from tools  import weather 
from tools.weather import weather
from tools.calculator import calculator
from tools.rag import rag
# -------------------------
# State
# -------------------------

class AgentState(TypedDict):

    question: str
    answer: str
    tool: str
    tool_input: str
    tool_result: str


# -------------------------
# LLM
# -------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0
)


# -------------------------
# LLM Node
# -------------------------

def llm_node(state: AgentState):

    question = state["question"]

    prompt = f"""
    You are an AI agent.

    User question:

    {question}

    Decide what to do.

    Available tools:

    1. calculator
    Use this for mathematical calculations.

    2. weather
    Use this for weather questions.

    3. rag
    Use this when the user asks about information
    contained in the PDF/document knowledge base.

    4. answer
    Use this for normal questions that don't require a tool.

    IMPORTANT:
    If the user asks something that should be answered
    from the PDF/document, you MUST use the rag tool.

    Return EXACTLY in this format:

    TOOL: calculator
    INPUT: 25 * 40

    OR

    TOOL: weather
    INPUT: Delhi

    OR

    TOOL: rag
    INPUT: What is Python?

    OR

    TOOL: answer
    INPUT: none
    """

    response = llm.invoke(prompt)

    text = response.content.strip()

    print("\nLLM Decision:")
    print(text)

    lines = text.splitlines()

    tool = "answer"
    tool_input = "none"

    for line in lines:

        if line.startswith("TOOL:"):
            tool = line.replace("TOOL:", "").strip()

        elif line.startswith("INPUT:"):
            tool_input = line.replace("INPUT:", "").strip()

    return {
        "tool": tool,
        "tool_input": tool_input
    }


# -------------------------
# Decision Function
# -------------------------

def decide_next(state: AgentState):

    tool = state["tool"]

    if tool == "calculator":
        return "calculator"

    elif tool == "weather":
        return "weather"
    elif tool == "rag":
        return "rag"


    else:
        return "final"


# -------------------------
# Calculator Node
# -------------------------

def calculator_node(state: AgentState):
    print('--------------------101')

    print("\nCalculator tool running...")

    result = calculator(state["tool_input"])

    print("Calculator result:", result)

    return {
        "tool_result": result
    }


# -------------------------
# Weather Node
# -------------------------

def weather_node(state: AgentState):

    print("\nWeather tool running...")

    result = weather(state["tool_input"])

    print("Weather result:", result)

    return {
        "tool_result": result
    }

# -------------------------
# RAG Node
# -------------------------

def rag_node(state: AgentState):

    print("RAG tool running...")

    result = rag(state["tool_input"])

    print("rag result:", result)

    return {
        "tool_result": result
    }

# -------------------------
# Final Node
# -------------------------

def final_node(state: AgentState):

    # Normal question
    if state["tool"] == "answer":

        response = llm.invoke(
            state["question"]
        )

        return {
            "answer": response.content
        }

    # Tool question
    prompt = f"""
Answer the user's question using the tool result.

User question:
{state["question"]}

Tool result:
{state["tool_result"]}

Give a clear and simple final answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# -------------------------
# Create Graph
# -------------------------

graph = StateGraph(AgentState)


# Add nodes

graph.add_node("llm", llm_node)

graph.add_node("calculator", calculator_node)

graph.add_node("weather", weather_node)

graph.add_node("rag", rag_node)

graph.add_node("final", final_node)


# -------------------------
# Edges
# -------------------------

graph.add_edge(START, "llm")


graph.add_conditional_edges(
    "llm",
    decide_next,
    {
        "calculator": "calculator",
        "weather": "weather",
        "rag":"rag",
        "final": "final"
    }
)


graph.add_edge("calculator", "final")

graph.add_edge("weather", "final")

graph.add_edge("rag", "final")

graph.add_edge("final", END)


# Compile

app = graph.compile()