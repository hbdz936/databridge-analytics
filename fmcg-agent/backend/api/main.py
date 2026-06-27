import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.graph.pipeline import pipeline, run_pipeline_with_timeout
from backend.graph.state import AgentState
from dotenv import load_dotenv
import asyncio

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "databridge-agent")

app = FastAPI(title="DataBridge Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    user_query: str
    refined_query: str
    generated_sql: str
    validation_result: str
    insights: str
    critic_feedback: str
    row_count: int
    query_results: list[dict] = []
    error: str | None

@app.get("/")
def health():
    return {"status": "ok", "service": "databridge-analytics"}

@app.post("/query", response_model=QueryResponse)
async def run_query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    initial_state: AgentState = {
        "user_query": request.question,
        "refined_query": "",
        "schema_context": "",
        "generated_sql": "",
        "validation_result": "",
        "query_results": [],
        "insights": "",
        "critic_feedback": "",
        "final_response": "",
        "error": None,
        "short_circuited": False
    }

    try:
        result = await run_pipeline_with_timeout(initial_state, timeout_seconds=60)

        return QueryResponse(
            user_query=result["user_query"],
            refined_query=result["refined_query"],
            generated_sql=result["generated_sql"],
            validation_result=result["validation_result"],
            insights=result["insights"],
            critic_feedback=result["critic_feedback"],
            row_count=len(result.get("query_results", [])),
            query_results=result.get("query_results", [])[:50],
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

@app.get("/sample-questions")
def sample_questions():
    return {
        "questions": [
            "What are the top 5 products by revenue this year?",
            "Which market has the highest sold quantity?",
            "Show me monthly sales trend for the Nutrition division",
            "Which customers are in the Brick & Mortar channel?",
            "Compare revenue between Sports and Nutrition categories"
        ]
    }