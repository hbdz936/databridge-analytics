from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Databricks SQL expert. Generate a valid Spark SQL query.

Rules:
- Always use fully qualified table names: fmcg.gold.table_name
- For revenue: JOIN fact_orders with dim_gross_price on product_code AND year (extract year from date)
- For customer info: JOIN fact_orders with dim_customers on customer_code
- For product info: JOIN fact_orders with dim_products on product_code
- Always add LIMIT 1000 unless asked for aggregations
- Return ONLY the SQL query, no explanation, no markdown backticks

Schema + Notes:
{schema_context}"""),
    ("human", "{refined_query}")
])

def sql_agent(state: AgentState) -> AgentState:
    chain = prompt | llm
    result = chain.invoke({
        "schema_context": state["schema_context"],
        "refined_query": state["refined_query"]
    })
    sql = result.content.strip().replace("```sql", "").replace("```", "").strip()
    return {
        **state,
        "generated_sql": sql
    }