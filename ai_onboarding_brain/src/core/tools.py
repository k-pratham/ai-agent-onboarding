from langchain_core.tools import tool
from ai_onboarding_brain.src.core.config import get_logger

try:
    from mcp_server.send_email.tools.send_email import tool_send_email
except ImportError:
    tool_send_email = None

logger = get_logger(__name__)

async def _notify_hr_on_failure(tool_name: str, error_msg: str):
    """ Escalate internally hidden anomalies directly to the HR admins """
    logger.error(f"Executing HR escalation for {tool_name} failure: {error_msg}")
    if tool_send_email:
        try:
            await tool_send_email("hr-admin@example.com", f"Agent Alert: {tool_name} Failed", f"The automated workflow encountered an error: {error_msg}")
        except Exception as e:
            logger.critical(f"Catastrophic failure: Could not even send HR admin alert: {e}")

@tool
async def extract_and_validate_document(file_path: str) -> str:
    """
    Reads a document off disk, parses it to Base64 (supporting PDFs via PyMuPDF),
    and sends it to the local vLLM nuMarkDown-8B-thinking engine for classification.
    """
    try:
        import os
        import base64
        import fitz  # PyMuPDF
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        logger.info(f"LangChain Tool: OCR Validation evaluating {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot locate attachment at {file_path}")
            
        base64_image = ""
        # Determine Parse logic
        if file_path.lower().endswith('.pdf'):
            logger.info("Executing PyMuPDF extraction wrapper on PDF format...")
            # Open PDF and render first page to PNG
            doc = fitz.open(file_path)
            if len(doc) == 0:
                raise ValueError("PDF is completely empty.")
            page = doc.load_page(0)
            pix = page.get_pixmap()
            image_bytes = pix.tobytes("png")
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
        else:
            # Assume it's an image
            with open(file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        # VLLM OpenAi wrapper natively supports Vision parameters
        vllm_base_url = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
        llm = ChatOpenAI(
            model="numarkdown-8b-thinking", # Target OCR explicitly
            temperature=0,
            openai_api_base=vllm_base_url,
            openai_api_key="vllm_key"
        )
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Specify exactly what type of Candidate HR document this is (e.g. PAN Card, Aadhaar, Resume, 10th Marksheet)."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]
        )
        
        logger.info("Dispatching Base64 visual payload to nuMarkDown engine via vLLM...")
        response = llm.invoke([message])
        return f"Classification Engine Result: {response.content}"
        
    except Exception as e:
        error_payload = f"OCR Validation failed on {file_path}. System trace: {str(e)}"
        await _notify_hr_on_failure("OCR Validation", error_payload)
        return f"Error executing tool: {error_payload}"

@tool
async def analyze_gap_tracker(cin: str) -> dict:
    """
    Performs gap analysis checking what candidate documents from the HR requirements are still missing.
    Queries the DOCUMENT_TRACKER dynamically against DOCUMENT_TYPE_MASTER.
    """
    try:
        logger.info(f"LangChain Tool: Dynamic Database Gap Tracker evaluating CIN: {cin}")
        from ai_onboarding_brain.src.core.database import SessionLocal
        from etl_pipeline.models.schema import CandidateInfo, DocumentTracker, DocumentTypeMaster
        
        db = SessionLocal()
        try:
            # Fetch candidate ID matching CIN
            candidate = db.query(CandidateInfo).filter(CandidateInfo.CIN == cin).first()
            if not candidate:
                return {"error": f"Candidate CIN {cin} does not exist in master DB."}
                
            # Grab all Mandatory standard documents (Just an example definition pulling all active master docs)
            expected_docs = db.query(DocumentTypeMaster).filter(DocumentTypeMaster.IS_ACTIVE == 1).all()
            
            # Grab all tracked documents for this candidate specifically
            tracked_docs = db.query(DocumentTracker).filter(DocumentTracker.CANDIDATE_ID == candidate.CANDIDATE_ID).all()
            
            # Calculate gap missing sets
            tracked_ids = [doc.DOCUMENT_TYPE_ID for doc in tracked_docs]
            missing_docs = []
            
            for expected in expected_docs:
                if expected.DOCUMENT_TYPE_ID not in tracked_ids:
                    missing_docs.append(expected.DOCUMENT_NAME)
                    
            status = "completed" if len(missing_docs) == 0 else "pending_documents"
            
            return {
                "cin": cin, 
                "candidate_name": candidate.CANDIDATE_NAME,
                "missing_documents": missing_docs, 
                "status": status
            }
        finally:
            db.close()
            
    except Exception as e:
        error_payload = f"Gap tracker database parse failure for {cin}. Trace: {str(e)}"
        await _notify_hr_on_failure("Gap Tracker", error_payload)
        return {"error": error_payload}

@tool
async def dispatch_followup_email(candidate_email: str, subject: str, draft_content: str) -> str:
    """
    Dispatches a followup or warning email communicating missing documents to the user directly!
    """
    try:
        logger.info(f"LangChain Tool: Dispatching email to {candidate_email}")
        if tool_send_email:
            return await tool_send_email(candidate_email, subject, draft_content)
        return f"Mocked email success to {candidate_email}"
    except Exception as e:
        error_payload = f"SMTP dispatch failed terminating logic. Trace: {str(e)}"
        await _notify_hr_on_failure("Email Dispatch", error_payload)
        return f"Error executing dispatch: {error_payload}"

# Registry of Tools passed directly to the Brain
AGENT_TOOLS = [
    extract_and_validate_document,
    analyze_gap_tracker,
    dispatch_followup_email
]
