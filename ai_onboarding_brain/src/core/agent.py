import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ai_onboarding_brain.src.core.tools import AGENT_TOOLS
from ai_onboarding_brain.src.core.checkpointer import OracleCheckpointer

# Configure standard Message state dictionary carrying conversation history
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Hook to VLLM exposed model (gpt-oss-20b per instructions)
vllm_base_url = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
llm = ChatOpenAI(
    model="gpt-oss-20b", 
    temperature=0, 
    openai_api_base=vllm_base_url,
    openai_api_key="vllm" # vLLM doesn't usually guard locally, but pass generic key
)

# Bind native generic HR tools back to the local model capabilities
llm_with_tools = llm.bind_tools(AGENT_TOOLS)

system_prompt = SystemMessage(content="""You are an autonomous HR Agent.
Your job is to orchestrate candidate document verification workflows.
You have access to tools that Validate Documents, run Gap Analysis, and directly Email Candidates.
Review candidate information and decide the next operation continuously based on missing artifacts.
""")

def run_agent(state: AgentState):
    """ Node issuing the call to the model """
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [system_prompt] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def route_condition(state: AgentState):
    """ Decide to run tools or Finish. """
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Construct Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", run_agent)
workflow.add_node("tools", ToolNode(AGENT_TOOLS))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", route_condition, ["tools", END])
workflow.add_edge("tools", "agent")

def get_compiled_orchestrator(db_session):
    """ Returns the compiled graph instance bound with the DB Checkpointer """
    checkpointer = OracleCheckpointer(db_session)
    app = workflow.compile(checkpointer=checkpointer)
    return app
