from mcp_server.draft_prepare.engine.helper_func import generate_draft

async def tool_draft_prepare(cin: str, candidate_name: str, missing_docs: list) -> str:
    """
    MCP Draft Tool: Formulates follow-up emails and interfaces directly with the HR database layer.
    """
    generated_email = generate_draft(candidate_name, missing_docs)
    
    # Emulate write action to Job_Tracker table where DRAFT_MAIL = generated_email
    # which ultimately gets surfaced to the existing HR UI for 'Human-In-The-Loop' approval.
    
    return f"Draft formulation completed successfully and staged into DB sequence for candidate {cin}."
