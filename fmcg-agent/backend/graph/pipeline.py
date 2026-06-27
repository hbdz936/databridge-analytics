from langgraph.graph import StateGraph, END
from backend.graph.state import AgentState
from backend.agents.orchestrator import orchestrator_agent
from backend.agents.schema_agent import schema_agent
from backend.agents.sql_agent import sql_agent
from backend.agents.validator_agent import validator_agent
from backend.agents.insight_agent import insight_agent
from backend.agents.critic_agent import critic_agent
import asyncio

SHORT_CIRCUIT_TOKENS = {"GREETING", "OFF_TOPIC", "AMBIGUOUS"}

def route_after_orchestrator(state: AgentState) -> str:
    if state.get("refined_query") in SHORT_CIRCUIT_TOKENS:
        return "insight"
    return "schema"

def route_after_validator(state: AgentState) -> str:
    return "insight"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("orchestrator", orchestrator_agent)
    graph.add_node("schema", schema_agent)
    graph.add_node("sql", sql_agent)
    graph.add_node("validator", validator_agent)
    graph.add_node("insight", insight_agent)
    graph.add_node("critic", critic_agent)

    graph.set_entry_point("orchestrator")

    # Skip schema/sql/validator entirely for greetings, off-topic, ambiguous input
    graph.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {"schema": "schema", "insight": "insight"}
    )

    graph.add_edge("schema", "sql")
    graph.add_edge("sql", "validator")
    graph.add_conditional_edges("validator", route_after_validator, {"insight": "insight"})
    graph.add_edge("insight", "critic")
    graph.add_edge("critic", END)

    return graph.compile()

pipeline = build_graph()


async def run_pipeline_with_timeout(initial_state: AgentState, timeout_seconds: int = 60) -> AgentState:
    """
    Runs the LangGraph pipeline in a background thread with a hard timeout.
    LangGraph's .invoke() is synchronous/blocking, so we offload it to a thread
    via asyncio.to_thread and enforce a timeout with asyncio.wait_for.
    """
    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(pipeline.invoke, initial_state),
            timeout=timeout_seconds
        )
        return result
    except asyncio.TimeoutError:
        return {
            **initial_state,
            "error": f"Pipeline timed out after {timeout_seconds} seconds. This usually happens when the Databricks SQL Warehouse is cold-starting. Please try again.",
            "validation_result": "failed",
            "insights": "Request timed out — the Databricks warehouse may be starting up. Please retry in a moment.",
            "critic_feedback": "N/A — pipeline did not complete in time."
        }
    except Exception as e:
        return {
            **initial_state,
            "error": f"Pipeline failed: {str(e)}",
            "validation_result": "failed",
            "insights": "An unexpected error occurred while processing your question.",
            "critic_feedback": "N/A — pipeline encountered an error."
        }