from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
from backend.db.databricks import SCHEMA_CONTEXT
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an orchestrator for an FMCG analytics system.
Your job is to understand the user's business question and rephrase it 
into a clear, precise analytical question.

The data is about a sports equipment + nutrition company merger.
Available data: orders, customers, products, pricing, dates.

Return ONLY the refined question, nothing else."""),
    ("human", "{user_query}")
])

def orchestrator_agent(state: AgentState) -> AgentState:
    chain = prompt | llm
    result = chain.invoke({"user_query": state["user_query"]})
    return {
        **state,
        "refined_query": result.content,
        "schema_context": SCHEMA_CONTEXT
    }