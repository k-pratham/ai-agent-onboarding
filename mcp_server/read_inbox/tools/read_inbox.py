from mcp_server.read_inbox.engine.helper_func import fetch_unread_candidate_replies

async def tool_read_inbox() -> str:
    """
    MCP Tool: Agent utilizes this to actively check the inbox for candidate replies.
    It fetches emails and initiates the cancelation of outstanding HR follow-up notifications.
    """
    emails = fetch_unread_candidate_replies()
    
    if not emails:
        return "No unread emails found in inbox."
        
    return f"Successfully fetched {len(emails)} unread candidate emails. Ready for parsing and gap analysis."
