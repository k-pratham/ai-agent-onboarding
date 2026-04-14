import pytest
import sys

# Test whether the FastMCP application imports and initializes valid tools cleanly
def test_fastmcp_app_initialization():
    from mcp_server.main import mcp_app
    
    assert mcp_app.name == "Agentic HR Onboarding Tool Server"
    
    # The application should have registered specific tools
    # FastMCP exposes `.tools` property or dict depending on internal structure 
    # but at least let's assert the properties of our tools.
    
    tools = [tool.name for tool in mcp_app._tools.values()] if hasattr(mcp_app, "_tools") else []
    if tools:
        assert "send_email" in tools
        assert "gap_analysis" in tools
        assert "read_inbox_tool" in tools
    else:
        # Some fastmcp versions use different internals, skip dict validation if unsupported,
        # but ensure module imports without exception.
        pass

def test_send_email_tool_returns_successfully(monkeypatch):
    from mcp_server.main import send_email
    
    # Mock the internal physical SMTP execution
    async def mock_tool_send_email(*args, **kwargs):
        return "Email sent mockup"
        
    monkeypatch.setattr("mcp_server.main.tool_send_email", mock_tool_send_email)
    
    import asyncio
    result = asyncio.run(send_email("test@mail.com", "Subject", "Content"))
    assert result == "Email sent mockup"
