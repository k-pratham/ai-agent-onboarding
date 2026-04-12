from mcp_server.gap_analysis.engine.helper_func import perform_gap_analysis

async def tool_gap_analysis(cin: str, db_required_docs: list, ocr_completed_docs: list) -> str:
    """
    MCP Gap Analysis Tool: 'Final checker' tracking which documents are missing vs received.
    """
    result = perform_gap_analysis(cin, ocr_completed_docs, db_required_docs)
    
    # System logic to update DOCUMENT_TRACKER marking valid files as 'complete'
    # Invalid/unmatched ones preserve their 'pending' db constraint.
    
    return f"Gap Analysis resolved. Outstanding pending documents: {', '.join(result['missing']) if result['missing'] else 'None'}"
