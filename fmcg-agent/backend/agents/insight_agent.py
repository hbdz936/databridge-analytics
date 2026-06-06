from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
import json
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior FMCG business analyst.
Given query results, generate clear business insights.

Format your response as:
**Key Finding:** One sentence summary
**Insights:**
- Bullet point observations (3-5 points)
**Recommendation:** One actionable recommendation

Keep it sharp and business-focused."""),
    ("human", """Business question: {refined_query}

Data results (first 20 rows):
{query_results}

Generate insights.""")
])

def insight_agent(state: AgentState) -> AgentState:
    if state.get("validation_result") == "failed":
        return {
            **state,
            "insights": "Could not generate insights — query execution failed."
        }
    
    results_preview = json.dumps(state["query_results"][:20], indent=2, default=str)
    
    chain = prompt | llm
    result = chain.invoke({
        "refined_query": state["refined_query"],
        "query_results": results_preview
    })
    return {
        **state,
        "insights": result.content
    }