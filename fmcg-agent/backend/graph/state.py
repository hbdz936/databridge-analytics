from typing import TypedDict, Optional

class AgentState(TypedDict):
    user_query: str
    refined_query: str
    schema_context: str
    generated_sql: str
    validation_result: str
    query_results: list[dict]
    insights: str
    critic_feedback: str
    final_response: str
    error: Optional[str]