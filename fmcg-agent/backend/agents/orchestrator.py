from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.graph.state import AgentState
from backend.db.databricks import SCHEMA_CONTEXT
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, timeout=30)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an orchestrator for an FMCG analytics system.
The data is about a sports equipment + nutrition company merger.
Available data: orders, customers, products, pricing, dates.

Classify the user's input, then respond with ONLY ONE of the following:

- If it is a greeting or casual remark (e.g. "hello", "how are you", "thanks"):
  respond with exactly: GREETING

- If it is unrelated to this business data — including weather, coding requests,
  writing or debugging scripts, general trivia, personal questions, math problems,
  translations, or asking the assistant to perform any task not about this dataset:
  respond with exactly: OFF_TOPIC

- If it is too vague to query even with reasonable interpretation (e.g. "tell me something", "show me data"):
  respond with exactly: AMBIGUOUS

- If it is a genuine analytical question answerable using orders, customers, products, pricing, or dates:
  respond with the refined, precise version of the question itself, as plain text.

Example 1:
Input: "which market sells the most"
Output: Which market has the highest total sold quantity across all orders?

Example 2:
Input: "how are you"
Output: GREETING

Example 3:
Input: "what's the weather like"
Output: OFF_TOPIC

Example 4:
Input: "write me a python script to sort a list"
Output: OFF_TOPIC

Example 5:
Input: "can you debug this code for me"
Output: OFF_TOPIC

Example 6:
Input: "what's 2+2"
Output: OFF_TOPIC

Example 7:
Input: "translate this sentence to french"
Output: OFF_TOPIC

Example 8:
Input: "tell me something"
Output: AMBIGUOUS

Never output the literal word VALID. Never explain your answer. Output only the single classification token, or the refined question text — nothing else."""),
    ("human", "{user_query}")
])

def orchestrator_agent(state: AgentState) -> AgentState:
    user_query = state["user_query"].strip()

    # Guard: empty or whitespace-only input
    if not user_query:
        return {
            **state,
            "refined_query": "OFF_TOPIC",
            "schema_context": SCHEMA_CONTEXT,
            "error": "Empty question received."
        }

    # Guard: extremely long input — truncate before sending to LLM
    if len(user_query) > 1000:
        user_query = user_query[:1000]

    try:
        chain = prompt | llm
        result = chain.invoke({"user_query": user_query})
        refined = result.content.strip()
    except Exception as e:
        return {
            **state,
            "refined_query": "OFF_TOPIC",
            "schema_context": SCHEMA_CONTEXT,
            "error": f"Orchestrator failed: {str(e)}"
        }

    if refined in ("GREETING", "OFF_TOPIC", "AMBIGUOUS"):
        return {
            **state,
            "refined_query": refined,
            "schema_context": SCHEMA_CONTEXT
        }

    return {
        **state,
        "refined_query": refined,
        "schema_context": SCHEMA_CONTEXT
    }