from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
from backend.db.databricks import run_query
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

fix_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Databricks SQL debugger.
A SQL query failed with an error. Fix it and return ONLY the corrected SQL.
No explanation, no markdown.

Schema:
{schema_context}

Original query:
{generated_sql}

Error:
{error}"""),
    ("human", "Fix the query.")
])

def validator_agent(state: AgentState) -> AgentState:
    sql = state["generated_sql"]
    
    try:
        results = run_query(sql)
        return {
            **state,
            "query_results": results,
            "validation_result": "success"
        }
    except Exception as e:
        # Auto-fix attempt
        chain = fix_prompt | llm
        fixed = chain.invoke({
            "schema_context": state["schema_context"],
            "generated_sql": sql,
            "error": str(e)
        })
        fixed_sql = fixed.content.strip().replace("```sql", "").replace("```", "").strip()
        
        try:
            results = run_query(fixed_sql)
            return {
                **state,
                "generated_sql": fixed_sql,
                "query_results": results,
                "validation_result": "fixed"
            }
        except Exception as e2:
            return {
                **state,
                "query_results": [],
                "validation_result": "failed",
                "error": str(e2)
            }