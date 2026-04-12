import os
import shutil
from mcp_server.ocr_classification.engine.helper_func import classify_document_type
from mcp_server.ocr_classification.utils.ocr import extract_text_from_file

async def tool_ocr_and_segregate(cin: str, file_path: str) -> str:
    """
    MCP Segregation Tool: Organizes candidate attachments into categories after validation.
    """
    ocr_text = extract_text_from_file(file_path)
    doc_type = classify_document_type(ocr_text)
    
    # Segregation schema implementation
    base_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    if doc_type in ['AADHAAR', 'PAN']:
        target_sub = "personal_details"
    elif doc_type == 'MARKSHEET':
        target_sub = "education"
    else:
        target_sub = "unmatched"
        
    target_dir = os.path.join(base_dir, target_sub)
    os.makedirs(target_dir, exist_ok=True)
    
    # Move payload
    new_path = os.path.join(target_dir, f"{doc_type}_{cin}_{file_name}")
    shutil.move(file_path, new_path)
    
    status = "complete" if target_sub != "unmatched" else "pending"
    return f"Validated {file_name}. Segregated to `{target_sub}` block. Sync status: {status}"
