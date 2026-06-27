from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
from backend.db.databricks import run_query
import time

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, timeout=30)

fix_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Databricks SQL debugger.
A SQL query failed with an error. Fix it and return ONLY the corrected SQL.
No explanation, no markdown, no backticks.

Schema:
{schema_context}

Original query:
{generated_sql}

Error message:
{error}

Common fixes:
- Check table names are fully qualified (fmcg.gold.table_name)
- Check column names exist in schema
- For date filtering, use YEAR(date) = 2024 or similar
- For Spark SQL, use datediff(current_date, date) not DATEDIFF
"""),
    ("human", "Return ONLY the fixed SQL query.")
])

def validator_agent(state: AgentState) -> AgentState:
    sql = state["generated_sql"]
    max_retries = 2
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            # Add timeout to query execution (30 seconds)
            results = run_query(sql)
            return {
                **state,
                "query_results": results,
                "validation_result": "success"
            }
        except Exception as e:
            error_msg = str(e)
            
            # If this is the last retry or a timeout, fail gracefully
            if retry_count >= max_retries:
                return {
                    **state,
                    "query_results": [],
                    "validation_result": "failed",
                    "error": f"Query failed after {max_retries + 1} attempts: {error_msg}"
                }
            
            # Try to fix the query
            retry_count += 1
            try:
                chain = fix_prompt | llm
                fixed_response = chain.invoke({
                    "schema_context": state["schema_context"],
                    "generated_sql": sql,
                    "error": error_msg
                })
                sql = fixed_response.content.strip().replace("```sql", "").replace("```", "").strip()
            except Exception as fix_error:
                # If fix attempt fails, move to next retry or fail
                if retry_count >= max_retries:
                    return {
                        **state,
                        "query_results": [],
                        "validation_result": "failed",
                        "error": f"SQL fix attempt failed: {str(fix_error)}"
                    }
                continue
    
    # Should not reach here, but failsafe
    return {
        **state,
        "query_results": [],
        "validation_result": "failed",
        "error": "Unknown validation error"
    }