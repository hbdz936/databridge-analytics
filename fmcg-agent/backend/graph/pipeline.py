from langgraph.graph import StateGraph, END
from backend.graph.state import AgentState
from backend.agents.orchestrator import orchestrator_agent
from backend.agents.schema_agent import schema_agent
from backend.agents.sql_agent import sql_agent
from backend.agents.validator_agent import validator_agent
from backend.agents.insight_agent import insight_agent
from backend.agents.critic_agent import critic_agent

def should_continue(state: AgentState) -> str:
    if state.get("validation_result") == "failed":
        return "insight"  # still go to insight, it handles failure gracefully
    return "insight"

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("orchestrator", orchestrator_agent)
    graph.add_node("schema", schema_agent)
    graph.add_node("sql", sql_agent)
    graph.add_node("validator", validator_agent)
    graph.add_node("insight", insight_agent)
    graph.add_node("critic", critic_agent)

    # Define edges
    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", "schema")
    graph.add_edge("schema", "sql")
    graph.add_edge("sql", "validator")
    graph.add_conditional_edges("validator", should_continue, {"insight": "insight"})
    graph.add_edge("insight", "critic")
    graph.add_edge("critic", END)

    return graph.compile()

pipeline = build_graph()