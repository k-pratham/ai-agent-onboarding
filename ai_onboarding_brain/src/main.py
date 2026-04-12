from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_onboarding_brain.src.routes.api import router as api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HR Agentic Onboarding Brain",
    description="Intelligent API orchestration for human-in-the-loop and ML pipeline automation.",
    version="1.0.0"
)

# Standard permissive CORS layer for easy binding to pre-existing HR UI Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    """
    System endpoint indicating Brain availability.
    """
    return {"status": "ok", "service": "onboarding_brain"}
