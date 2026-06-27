from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, timeout=30)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a critical reviewer for an AI analytics system.
Review the full pipeline output and assess quality.

Score each dimension 1-5:
- SQL Correctness: Does the SQL correctly answer the question?
- Insight Quality: Are insights specific, accurate, non-obvious?
- Completeness: Does the response fully address the user's question?

Format:
**SQL Correctness:** X/5 — reason
**Insight Quality:** X/5 — reason  
**Completeness:** X/5 — reason
**Overall:** X/5
**Suggestion:** One improvement if overall < 4, else "Output is satisfactory." """),
    ("human", """Original question: {user_query}
Refined question: {refined_query}
Generated SQL: {generated_sql}
Validation: {validation_result}
Insights: {insights}

Review this output.""")
])

def critic_agent(state: AgentState) -> AgentState:
    if state.get("short_circuited"):
        return {
            **state,
            "critic_feedback": "N/A — input was outside the analytical scope of this dataset, so no SQL was generated or evaluated.",
            "final_response": state["insights"]
        }

    try:
        chain = prompt | llm
        result = chain.invoke({
            "user_query": state["user_query"],
            "refined_query": state["refined_query"],
            "generated_sql": state["generated_sql"],
            "validation_result": state["validation_result"],
            "insights": state["insights"]
        })
        feedback = result.content
    except Exception as e:
        feedback = f"Critic evaluation failed: {str(e)}"

    return {
        **state,
        "critic_feedback": feedback,
        "final_response": state["insights"]
    }