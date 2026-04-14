# Agentic HR Onboarding System Documentation

This document provides a comprehensive overview of the **Agentic HR Onboarding System**. It details the overarching architecture, the distinct modular components, and the step-by-step logical workflow that routes candidates from Excel ingestion up to autonomous document tracking and agentic verification.

---

## 1. System Architecture Overview

The system is built sequentially onto a Model Context Protocol (MCP) backbone, orchestrated dynamically using LangGraph, and layered with a `FastAPI` service ensuring tight **Human-In-The-Loop (HITL)** capabilities. 

### High-Level Layers
- **ETL Pipeline**: Synchronizes raw static tracker documents (Excel) with a centralized Oracle Database backend.
- **FastMCP Subsystems (mcp_server)**: Wraps internal scripts (SMTP tools, mailbox crawlers) and LLM-evaluators (OCR validators) using a native STDIO server making them universally consumable plugins.
- **AI Onboarding Brain**: The central FastAPI interface scaling internal routes (HR interaction), the database checkpointer, and a stateful LangGraph agent logic. 

---

## 2. Directory & File Breakdown

### **A. Database & Initialization Scripts**
- `etl_pipeline/models/schema.py`: Contains the `SQLAlchemy` relational maps. Holds definitions for entities like `CandidateInfo`, `JobTracker`, `DocumentTracker` and specifically the core memory cache for operations: `AgentState`. 
- `scripts/seed_master_data.py`: Developer utility script. Easily constructs mapped integer constants for statuses (`mail sent`, `verified`) or core application job profiles directly into the SQL Database.
- `requirements.txt`: Exposes backend dependencies inclusive of Oracle's DB mapping library, `langgraph`, `fastAPI`, and `fastmcp`.

### **B. The Brain (`ai_onboarding_brain/`)**
The logic nexus orchestrating web traffic and Language Model reasoning.

#### **Backend Configs & SQL Maps**
- `src/core/config.py`: The settings mapper pulling directly from the user's local variables (e.g., SMTP keys, Oracle URIs) and exposes strictly typed fallback values bridging DB constraints. 
- `src/core/database.py`: Constructs the `SessionLocal` database connection pool and acts as a FastAPI `Depends` hook provider (`get_db()`).

#### **Agent Definitions (`src/core/`)**
- `checkpointer.py`: Houses the `OracleCheckpointer`. Natively implements `BaseCheckpointSaver`, ensuring deep persistence logic across the `thread_id` so LangGraph never drops context inside the SQL memory.
- `tools.py`: Wraps internal MCP tools inside the native LangChain `@tool` decorator, transforming basic Python functions into LLM-interpretable JSON parameters.
- `agent.py`: Constructs the `StateGraph`. Implements the continuous verification loop binding local `vLLM (gpt-oss-20b)` to our tools using `ChatOpenAI`. 

#### **Services & Routing (`src/routes/` & `src/services/`)**
- `api.py`: FastAPI endpoints exposing analytical and transactional capabilities directly to an external HR UI layout. Contains endpoints like `/dashboard/pending-drafts`.
- `hr_service.py`: Contains transactional procedures like `process_draft_approval`. Resolves SQL flags and generates subsequent +2 days "follow up" sequences. 

### **C. The Distributed Servers (`mcp_server/`)**
- `main.py`: Creates the standalone `FastMCP` application. It isolates system execution hooks providing seamless background routing via STDIO to internal tooling blocks (like the `send_email` component).
- `send_email/tools/send_email.py`: Exposes physical SMTP commands wrapped against `smtplib`.

---

## 3. End-to-End Logical Flow

### Phase 1: Intake Tracking (ETL DAG)
1. **Extraction**: A CRON scheduling layer drops into `etl_pipeline` scanning external file drops (like `Offer_tracker.xlsx`).
2. **Synchronization**: Raw records sync into the database modifying entries for `CANDIDATE_INFO`.
3. **Queue Creation**: Automatically generates initial state entries pushing into the `JOB_TRACKER` denoting a required "mail sent" operation parsing the 60-day Joiner rule. 

### Phase 2: Autonomous Intelligence (The Agent Loop)
1. The `read_inbox` module (triggered externally) aggregates attachments to specific candidate CINs.
2. The trigger resolves hitting `agent.py`. The `vLLM` proxy boots and examines the prompt.
3. The Graph loops parsing missing documentation against `Gap Analytics`.
4. The orchestration loops over our exposed `@tools` inside `tools.py` continuously generating `AgentState` snapshots persisted accurately via `checkpointer.py`.
5. If anomalies arise, the Agent writes draft emails queuing them against the DB state for manual inspection.

### Phase 3: Human Verification (The HR Loop)
1. HR personnel open the frontend parsing `/dashboard/pending-drafts`.
2. The system fetches joined mappings from the SQL constraints.
3. HR triggers an approval on a requested anomaly draft modifying `hr_service.py`. 
4. The backend hits the FastMCP hook natively `await tool_send_email()`.
5. DB transactions modify status vectors internally creating a 48-hour follow loop tracking the lifecycle natively.
