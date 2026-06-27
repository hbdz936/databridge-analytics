from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
import json

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, timeout=30)

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

SHORT_CIRCUIT_RESPONSES = {
    "GREETING": "Hi! I'm an analytics assistant for FMCG sales data. Ask me about revenue, top products, customer markets, or sales trends — for example, \"Which market has the highest sold quantity?\"",
    "OFF_TOPIC": "I can only answer questions about this FMCG dataset — orders, customers, products, pricing, and dates. Try asking something like \"What are the top 5 products by revenue?\"",
    "AMBIGUOUS": "That question is a bit too broad for me to turn into a query. Could you specify what you'd like to know — for example a product, market, time period, or metric like revenue or quantity sold?"
}

def insight_agent(state: AgentState) -> AgentState:
    refined = state.get("refined_query", "")

    # Short-circuit cases — never reached SQL/Validator
    if refined in SHORT_CIRCUIT_RESPONSES:
        return {
            **state,
            "insights": SHORT_CIRCUIT_RESPONSES[refined],
            "short_circuited": True
        }

    if state.get("validation_result") == "failed":
        return {
            **state,
            "insights": "Could not generate insights — query execution failed."
        }

    results_preview = json.dumps(state["query_results"][:20], indent=2, default=str)

    try:
        chain = prompt | llm
        result = chain.invoke({
            "refined_query": state["refined_query"],
            "query_results": results_preview
        })
        insights = result.content
    except Exception as e:
        insights = f"Insight generation failed: {str(e)}"

    return {
        **state,
        "insights": insights
    }