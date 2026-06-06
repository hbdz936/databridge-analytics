# FMCG Multi-Agent Analytics System

![Stack](https://img.shields.io/badge/LangGraph-Agent_Pipeline-orange) ![Stack](https://img.shields.io/badge/Databricks-Unity_Catalog-red) ![Stack](https://img.shields.io/badge/Groq-LLaMA_3.1-blue) ![Stack](https://img.shields.io/badge/FastAPI-Backend-green) ![Stack](https://img.shields.io/badge/React-Frontend-cyan)

A natural language analytics system built on top of a unified FMCG data lake. Ask a business question in plain English — the system figures out the SQL, runs it against live Databricks data, and returns structured business insights with a self-evaluated quality score.

---

## The Problem

A sports equipment company acquired a nutrition startup. Both had different schemas, different data formats, and different reporting systems. The goal: unify their analytics so any business question can be answered from a single interface — without writing SQL.

---

## How It Works

Every query goes through a 6-agent pipeline. Each agent has one job and passes its output to the next via a shared state object managed by LangGraph.

```
Plain English Question
        │
        ▼
  ┌─────────────────┐
  │  ORCHESTRATOR   │  Understands intent. Rewrites the question into a
  │                 │  precise analytical query with the right scope.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  SCHEMA AGENT   │  Reads the Gold layer schema. Decides which tables
  │                 │  to JOIN and which columns to use.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   SQL AGENT     │  Writes a valid Spark SQL query using fully
  │                 │  qualified table names (fmcg.gold.*).
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   VALIDATOR     │  Executes the SQL on Databricks. If it fails,
  │                 │  it reads the error, fixes the query, and retries.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  INSIGHT AGENT  │  Reads the query results and writes a business
  │                 │  intelligence report: key finding + bullets + recommendation.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  CRITIC AGENT   │  Reviews the full pipeline output. Scores SQL
  │                 │  correctness, insight quality, and completeness
  │                 │  out of 5. Flags what to improve.
  └─────────────────┘
```

---

## System Architecture

```
┌──────────────────────────────────────────────┐
│              React Frontend                  │
│  Terminal UI · Agent Trace · SQL Viewer      │
│  Intelligence Report · Critic Scorecard      │
└─────────────────────┬────────────────────────┘
                      │ HTTP POST /query
                      ▼
┌──────────────────────────────────────────────┐
│              FastAPI Backend                 │
│         /query  /docs  /sample-questions     │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│         LangGraph State Machine              │
│                                              │
│  Orchestrator → Schema → SQL → Validator     │
│                    → Insight → Critic        │
│                                              │
│  Shared AgentState flows through all nodes  │
│  LangSmith traces every step                │
└─────────────────────┬────────────────────────┘
                      │ Databricks SQL Connector
                      ▼
┌──────────────────────────────────────────────┐
│       Databricks Unity Catalog               │
│              fmcg.gold                       │
│                                              │
│  fact_orders · dim_customers · dim_products  │
│  dim_gross_price · dim_date                  │
└──────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Framework | LangGraph | Stateful multi-agent graph with conditional edges and shared state |
| LLM | Groq · LLaMA 3.1 8B | ~800 tok/s — full pipeline completes in under 30s |
| LLM Orchestration | LangChain Core | Prompt templates and chain composition |
| Observability | LangSmith | Per-agent traces, token usage, latency breakdown |
| Data Warehouse | Databricks Unity Catalog | Live Delta tables in medallion architecture |
| SQL Connector | databricks-sql-connector | JDBC connection to Databricks SQL Warehouse |
| Backend | FastAPI + Uvicorn | Async REST API with auto-generated docs |
| Frontend | React 18 + Vite | Component-based UI with fast HMR |

---

## Data Layer (Gold Schema)

```sql
fmcg.gold.fact_orders       — date, product_code, customer_code, sold_quantity
fmcg.gold.dim_customers     — customer_code, customer, market, platform, channel
fmcg.gold.dim_products      — product_code, division, category, product, variant
fmcg.gold.dim_gross_price   — product_code, price_inr, year
fmcg.gold.dim_date          — month_start_date, year, month_name, quarter
```

Built in Phase 1 using a Bronze → Silver → Gold medallion pipeline on Databricks with PySpark and Delta tables.

---

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
# Add credentials to backend/.env (see below)
cd ..
python backend/run.py        # → localhost:8000

# Frontend
cd frontend
npm install
npm run dev                  # → localhost:5173
```

**`backend/.env`**
```env
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-personal-access-token
GROQ_API_KEY=your-groq-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=fmcg-agent
```

---

## Phase Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1 | ✅ Complete | Medallion pipeline — Bronze → Silver → Gold on Databricks |
| Phase 2 | ✅ Complete | 6-agent LangGraph system + FastAPI + React terminal UI |