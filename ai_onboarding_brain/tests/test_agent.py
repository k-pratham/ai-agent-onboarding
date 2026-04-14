import pytest
from unittest.mock import MagicMock
from langchain_core.messages import HumanMessage
from ai_onboarding_brain.src.core.agent import get_compiled_orchestrator
from ai_onboarding_brain.src.core.checkpointer import OracleCheckpointer

def test_agent_checkpointer_storage_execution(monkeypatch):
    """
    Simulates calling the compiled graph with dummy Oracle bindings, 
    ensuring that graph checkpoint state updates successfully hit the database.
    """
    mock_db = MagicMock()
    
    # Avoid truly calling Local vLLM during unit tests!
    async def mock_invoke(*args, **kwargs):
        from langchain_core.messages import AIMessage
        return AIMessage(content="I've analyzed the gap and documents. Completed.")
        
    monkeypatch.setattr("ai_onboarding_brain.src.core.agent.llm_with_tools.invoke", mock_invoke)

    # Initialize agent via generic factory
    app = get_compiled_orchestrator(mock_db)
    
    config = {"configurable": {"thread_id": "CANDIDATE_100"}}
    
    # 1. Execute StateGraph run targeting specific output schema
    result = app.invoke({"messages": [HumanMessage(content="Candidate CIN100 uploaded their files.")]}, config=config)
    
    # 2. Check the output message
    assert len(result["messages"]) >= 2 # System + Human + AI
    assert "I've analyzed the gap" in result["messages"][-1].content
    
    # 3. Assert Checkpoint interactions (Since Checkpointer directly calls db.add() mapped to DB instance)
    assert mock_db.add.called
    assert mock_db.commit.called
    
    # We can inspect the specific object added to verify it matches our custom schema definition
    added_obj = mock_db.add.call_args[0][0]
    
    assert added_obj.THREAD_ID == "CANDIDATE_100"
    assert added_obj.STATE_PAYLOAD is not None
