from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a schema expert for an FMCG Databricks Gold layer.
Given a business question, identify which tables and columns are needed.

Schema:
{schema_context}

Return a brief note on which tables to JOIN and which columns to use.
Be concise — 3-5 lines max."""),
    ("human", "{refined_query}")
])

def schema_agent(state: AgentState) -> AgentState:
    chain = prompt | llm
    result = chain.invoke({
        "schema_context": state["schema_context"],
        "refined_query": state["refined_query"]
    })
    return {
        **state,
        "schema_context": state["schema_context"] + "\n\nSchema Agent Notes:\n" + result.content
    }