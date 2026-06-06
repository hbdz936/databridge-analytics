from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.graph.pipeline import pipeline
from backend.graph.state import AgentState
import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing — auto-enabled via .env vars
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "fmcg-agent")

app = FastAPI(title="FMCG Multi-Agent Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
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
    error: str | None

@app.get("/")
def health():
    return {"status": "ok", "service": "fmcg-agent"}

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
        "error": None
    }

    try:
        result = pipeline.invoke(initial_state)
        return QueryResponse(
            user_query=result["user_query"],
            refined_query=result["refined_query"],
            generated_sql=result["generated_sql"],
            validation_result=result["validation_result"],
            insights=result["insights"],
            critic_feedback=result["critic_feedback"],
            row_count=len(result["query_results"]),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample-questions")
def sample_questions():
    return {
        "questions": [
            "What are the top 5 products by revenue this year?",
            "Which market has the highest sold quantity?",
            "Show me monthly sales trend for the Nutrition division",
            "Which customers are in the Brick & Mortar channel?",
            "Compare revenue between sports and nutrition categories"
        ]
    }