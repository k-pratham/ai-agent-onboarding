"""
Demo Runner — Airflow-free entry point for the HR Agentic Onboarding System.

Replaces the three Airflow DAGs with a single interactive script:
  1. ETL Pipeline  (excel_etl_dag  — normally 10 PM IST)
  2. Mail Drafting (mail_draft_dag — normally 9 AM IST)
  3. Inbox Reader  (inbox_reader_dag — normally 9 PM IST)

Usage:
    python -m scripts.run_demo                     # run all steps
    python -m scripts.run_demo --step etl          # run only the ETL step
    python -m scripts.run_demo --step draft        # run only the mail drafting step
    python -m scripts.run_demo --step inbox        # run only the inbox reader step
    python -m scripts.run_demo --step seed         # seed master data only
    python -m scripts.run_demo --step api          # start the FastAPI server only
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime, date, timedelta

# ---------------------------------------------------------------------------
# Bootstrap: make sure the project root is on sys.path so all packages resolve
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("demo_runner")

# ---------------------------------------------------------------------------
# Config helpers (reuse existing config infrastructure)
# ---------------------------------------------------------------------------
from mcp_server.constants.common_functions import get_config, get_db_uri

DB_URI = get_db_uri()
EXCEL_PATH = os.getenv(
    "EXCEL_PATH",
    os.path.join(PROJECT_ROOT, "etl_pipeline", "excel_offer_tracker", "Offer_tracker.xlsx"),
)


def _get_db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(DB_URI, pool_pre_ping=True, pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    return Session()


def _run_async(coro):
    """Run an async coroutine in a sync context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ===================================================================
# STEP 0 — Seed master data
# ===================================================================
def run_seed():
    logger.info("=" * 60)
    logger.info("STEP 0: Seeding master data")
    logger.info("=" * 60)
    from scripts.seed_master_data import seed_data

    seed_data()
    logger.info("Seed complete.\n")


# ===================================================================
# STEP 1 — ETL Pipeline  (replaces excel_etl_dag)
# ===================================================================
def run_etl():
    logger.info("=" * 60)
    logger.info("STEP 1: ETL Pipeline — Excel → CANDIDATE_INFO + JOB_TRACKER")
    logger.info("=" * 60)

    from etl_pipeline.extract.excel_reader import extract_excel_data
    from etl_pipeline.transform.transformer import transform_candidate_data
    from etl_pipeline.load.db_loader import load_data

    if not os.path.exists(EXCEL_PATH):
        logger.error(f"Excel file not found at: {EXCEL_PATH}")
        logger.info("Set the EXCEL_PATH env var or place Offer_tracker.xlsx at the expected location.")
        return

    logger.info(f"Reading Excel from: {EXCEL_PATH}")
    raw_data = extract_excel_data(EXCEL_PATH)

    logger.info("Transforming data (CIN generation, row hashing, column mapping)…")
    transformed_data = transform_candidate_data(raw_data)
    logger.info(f"Transformed {len(transformed_data)} rows from {len(raw_data)} sheets.")

    logger.info("Loading into database…")
    session = _get_db_session()
    try:
        load_data(session, transformed_data)
    finally:
        session.close()

    logger.info("ETL Pipeline complete.\n")


# ===================================================================
# STEP 2 — Mail Drafting  (replaces mail_draft_dag)
# ===================================================================
def run_mail_draft():
    logger.info("=" * 60)
    logger.info("STEP 2: Mail Drafting — Generate drafts for pending jobs")
    logger.info("=" * 60)

    from etl_pipeline.models.schema import (
        JobTracker, CandidateInfo, DocumentTypeMaster, DocumentTracker, MailTypeMaster,
    )

    session = _get_db_session()
    today = date.today()

    try:
        pending_jobs = session.query(JobTracker, CandidateInfo).join(
            CandidateInfo, JobTracker.CANDIDATE_ID == CandidateInfo.CANDIDATE_ID
        ).filter(
            JobTracker.JOB_TYPE_ID.in_([1, 2]),
            JobTracker.STATUS_ID == 1,
            JobTracker.ACTION_DATE <= today,
        ).all()

        logger.info(f"Found {len(pending_jobs)} pending jobs with ACTION_DATE <= {today}")

        drafted = 0
        for job, candidate in pending_jobs:
            candidate_type_id = candidate.CANDIDATE_TYPE_ID or 2
            candidate_name = candidate.CANDIDATE_NAME or candidate.CIN
            cin = candidate.CIN

            # Fetch mail template
            mail_type = "initial_documents" if job.JOB_TYPE_ID == 1 else "followup_documents"
            template_rec = session.query(MailTypeMaster).filter(
                MailTypeMaster.MAIL_TYPE == mail_type,
                MailTypeMaster.IS_ACTIVE == 1,
            ).first()
            mail_template = template_rec.MAIL_DESCRIPTION if template_rec else None

            # Get missing docs
            type_col = {1: "FRESHER", 2: "EXPERIENCE", 3: "DEV_PARTNER"}.get(candidate_type_id, "EXPERIENCE")
            required = session.query(DocumentTypeMaster).filter(
                DocumentTypeMaster.IS_ACTIVE == 1,
                getattr(DocumentTypeMaster, type_col) == 1,
            ).all()
            tracked = session.query(DocumentTracker).filter(
                DocumentTracker.CANDIDATE_ID == candidate.CANDIDATE_ID,
                DocumentTracker.IS_ACTIVE == 1,
            ).all()
            verified_ids = {d.DOCUMENT_TYPE_ID for d in tracked if d.STATUS_ID in (5, 7)}
            missing_docs = [d.DOCUMENT_NAME for d in required if d.DOCUMENT_TYPE_ID not in verified_ids]

            if not missing_docs and job.JOB_TYPE_ID == 2:
                job.STATUS_ID = 7
                job.UPDATED_ON = today
                logger.info(f"  CIN {cin}: No missing docs, marking follow-up complete.")
                continue

            # Generate draft (try LLM, fall back to template)
            try:
                from mcp_server.draft_prepare.engine.helper_func import generate_draft
                draft = generate_draft(candidate_name, missing_docs, cin, mail_template)
            except Exception:
                doc_list = "\n".join(f"  - {d}" for d in missing_docs)
                draft = (
                    f"Dear {candidate_name},\n\n"
                    f"As part of your onboarding (CIN: {cin}), please submit:\n{doc_list}\n\n"
                    f"Reply with attachments. Include your CIN in the subject.\n\n"
                    f"Regards,\nHR Onboarding Team"
                )

            job.DRAFT_MAIL = draft
            job.STATUS_ID = 2            # Mail Drafted
            job.HUMAN_ACTION_REQUIRED = 1
            job.UPDATED_ON = today
            drafted += 1
            logger.info(f"  CIN {cin}: Draft generated for Job {job.JOB_ID}")

        session.commit()
        logger.info(f"Mail Drafting complete. Drafted {drafted} email(s).\n")
    except Exception as e:
        session.rollback()
        logger.error(f"Mail drafting failed: {e}")
        raise
    finally:
        session.close()


# ===================================================================
# STEP 3 — Inbox Reader  (replaces inbox_reader_dag)
# ===================================================================
def run_inbox_reader():
    logger.info("=" * 60)
    logger.info("STEP 3: Inbox Reader — Read replies, save attachments, trigger agent")
    logger.info("=" * 60)

    from mcp_server.read_inbox.tools.read_inbox import tool_read_inbox
    from mcp_server.save_attachment.tools.save_attachment import tool_save_attachment

    inbox_result = _run_async(tool_read_inbox())

    if inbox_result.get("status") == "empty":
        logger.info("No unread emails found. Skipping.\n")
        return

    candidates = inbox_result.get("candidates", [])
    logger.info(f"Found {len(candidates)} distinct candidate(s) with replies.")

    for cdata in candidates:
        cin = cdata["cin"]
        has_attachments = cdata["has_attachments"]
        attachments = cdata.get("attachments", [])
        job_id = cdata.get("job_id")

        if not has_attachments:
            logger.info(f"  CIN {cin}: No attachments — follow-up deactivated.")
            continue

        saved = []
        for att in attachments:
            res = _run_async(tool_save_attachment(cin, att["filename"], att["data"], job_id))
            saved.append(res)
            logger.info(f"  CIN {cin}: Saved {att['filename']}")

        # Trigger the LangGraph agent
        logger.info(f"  CIN {cin}: Triggering agent for {len(saved)} attachment(s)…")
        try:
            _trigger_agent(cin, cdata["candidate_id"], saved)
        except Exception as e:
            logger.error(f"  CIN {cin}: Agent failed — {e}")

    logger.info("Inbox Reader complete.\n")


def _trigger_agent(cin: str, candidate_id: int, saved_files: list):
    from ai_onboarding_brain.src.core.agent import get_compiled_orchestrator
    from ai_onboarding_brain.src.core.database import SessionLocal
    from langchain_core.messages import HumanMessage

    db = SessionLocal()
    try:
        orchestrator = get_compiled_orchestrator(db)
        config = {"configurable": {"thread_id": f"CANDIDATE_{cin}"}}
        prompt = (
            f"Candidate CIN {cin} has uploaded {len(saved_files)} document(s). "
            f"Process each: OCR classification, identity validation, gap analysis, "
            f"and draft a follow-up if documents are missing."
        )
        result = orchestrator.invoke(
            {"messages": [HumanMessage(content=prompt)]}, config=config,
        )
        logger.info(f"  CIN {cin}: Agent finished ({len(result['messages'])} messages).")
    finally:
        db.close()


# ===================================================================
# STEP 4 — Start FastAPI server (for HR dashboard / approvals)
# ===================================================================
def run_api():
    logger.info("=" * 60)
    logger.info("STEP 4: Starting FastAPI Brain server on http://0.0.0.0:8080")
    logger.info("=" * 60)
    logger.info("Swagger docs → http://localhost:8080/docs")
    logger.info("Health check → http://localhost:8080/health\n")

    import uvicorn
    uvicorn.run(
        "ai_onboarding_brain.src.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )


# ===================================================================
# CLI
# ===================================================================
STEPS = {
    "seed":  ("Seed master data",            run_seed),
    "etl":   ("ETL Pipeline",                run_etl),
    "draft": ("Mail Drafting",               run_mail_draft),
    "inbox": ("Inbox Reader + Agent",        run_inbox_reader),
    "api":   ("FastAPI Server",              run_api),
}


def run_all():
    """Run the full demo pipeline: seed → etl → draft → inbox → api."""
    run_seed()
    run_etl()
    run_mail_draft()
    run_inbox_reader()
    run_api()


def main():
    parser = argparse.ArgumentParser(
        description="HR Agentic Onboarding — Demo Runner (no Airflow required)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available steps:
  seed   — Seed the master lookup tables (StatusMaster, JobTypeMaster, etc.)
  etl    — Run the ETL pipeline (Excel → DB)
  draft  — Run the mail-drafting step (generate drafts for pending jobs)
  inbox  — Run the inbox reader (read emails, save attachments, trigger agent)
  api    — Start the FastAPI server for the HR dashboard

Examples:
  python -m scripts.run_demo                  # run everything
  python -m scripts.run_demo --step seed etl  # seed then ETL only
  python -m scripts.run_demo --step api       # just start the API
        """,
    )
    parser.add_argument(
        "--step",
        nargs="+",
        choices=list(STEPS.keys()),
        help="Run specific step(s) instead of the full pipeline.",
    )
    args = parser.parse_args()

    logger.info("HR Agentic Onboarding System — Demo Runner")
    logger.info(f"Project root : {PROJECT_ROOT}")
    logger.info(f"DB URI       : {DB_URI}")
    logger.info(f"Excel path   : {EXCEL_PATH}")
    logger.info("")

    if args.step:
        for step_name in args.step:
            label, fn = STEPS[step_name]
            fn()
    else:
        run_all()

    logger.info("Demo Runner finished.")


if __name__ == "__main__":
    main()
