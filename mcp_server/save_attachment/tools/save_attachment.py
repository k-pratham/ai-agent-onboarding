from mcp_server.save_attachment.engine.helper_func import store_attachment

async def tool_save_attachment(cin: str, file_name: str, base64_data: str) -> str:
    """
    MCP Tool: Used by the agent to persist an incoming candidate attachment to disk 
    before performing OCR classification or Gap Analysis on it.
    
    Expects base64 encoded file input.
    """
    import base64
    
    try:
        file_bytes = base64.b64decode(base64_data)
        filepath = store_attachment(cin, file_name, file_bytes)
        
        # Placeholer for: "Append record in Document tracker with metadata: 'pending'"
        
        return f"Attachment {file_name} for CIN {cin} secured at {filepath}. Pending OCR Validation."
    except Exception as e:
        return f"Attachment extraction failed: {str(e)}"
