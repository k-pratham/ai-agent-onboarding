import json
from datetime import datetime, timezone
from typing import Optional, Iterator, Tuple, Dict, Any

from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata, CheckpointTuple
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from sqlalchemy.orm import Session

from etl_pipeline.models.schema import AgentState

class OracleCheckpointer(BaseCheckpointSaver):
    """
    A custom LangGraph Checkpointer that persists Agent State graphs
    into the Oracle SQL Database via our SQLAlchemy session.
    """
    def __init__(self, db_session: Session):
        super().__init__()
        self.db = db_session
        self.serde = JsonPlusSerializer()

    def put(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: dict) -> dict:
        try:
            thread_id = config["configurable"]["thread_id"]
            checkpoint_id = checkpoint["id"]
            
            parent_id = checkpoint.get("parent_id")
            
            state_payload = self.serde.dumps(checkpoint).decode('utf-8')
            metadata_payload = self.serde.dumps(metadata).decode('utf-8')
            
            from sqlalchemy.sql import func
            new_state = AgentState(
                THREAD_ID=thread_id,
                CHECKPOINT_ID=checkpoint_id,
                PARENT_CHECKPOINT_ID=parent_id,
                STATE_PAYLOAD=state_payload,
                METADATA_PAYLOAD=metadata_payload,
                UPDATED_ON=func.now()
            )
            
            self.db.add(new_state)
            self.db.commit()
            
            return {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id,
                    "checkpoint_ns": config["configurable"].get("checkpoint_ns", "")
                }
            }
        except Exception as e:
            self.db.rollback()
            # We don't want to crash the LangGraph engine entirely, but state failure is critical.
            print(f"Checkpointer Put Error: {str(e)}")
            raise e

    def put_writes(self, config: dict, writes: list[Tuple[str, Any]], task_id: str) -> None:
        """ Supports storing pending writes, optionally implemented for advanced parallel flows """
        pass
        
    def get_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        try:
            thread_id = config["configurable"]["thread_id"]
            checkpoint_id = config["configurable"].get("checkpoint_id")
            
            query = self.db.query(AgentState).filter(AgentState.THREAD_ID == thread_id)
            if checkpoint_id:
                query = query.filter(AgentState.CHECKPOINT_ID == checkpoint_id)
            
            record = query.order_by(AgentState.UPDATED_ON.desc()).first()
            
            if not record:
                return None
                
            checkpoint = self.serde.loads(record.STATE_PAYLOAD.encode('utf-8'))
            metadata = self.serde.loads(record.METADATA_PAYLOAD.encode('utf-8'))
            
            return CheckpointTuple(
                config={
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_id": record.CHECKPOINT_ID,
                        "checkpoint_ns": config["configurable"].get("checkpoint_ns", "")
                    }
                },
                checkpoint=checkpoint,
                metadata=metadata,
                parent_config={
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_id": record.PARENT_CHECKPOINT_ID,
                    }
                } if record.PARENT_CHECKPOINT_ID else None,
                pending_writes=[]
            )
        except Exception as e:
            print(f"Checkpointer Get Error: {str(e)}")
            return None

    def list(self, config: dict, filter: dict = None, before: dict = None, limit: int = None) -> Iterator[CheckpointTuple]:
        try:
            thread_id = config["configurable"]["thread_id"]
            query = self.db.query(AgentState).filter(AgentState.THREAD_ID == thread_id).order_by(AgentState.UPDATED_ON.desc())
            
            if limit:
                query = query.limit(limit)
                
            records = query.all()
            for record in records:
                checkpoint = self.serde.loads(record.STATE_PAYLOAD.encode('utf-8'))
                metadata = self.serde.loads(record.METADATA_PAYLOAD.encode('utf-8'))
                
                yield CheckpointTuple(
                    config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.CHECKPOINT_ID}},
                    checkpoint=checkpoint,
                    metadata=metadata,
                    parent_config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.PARENT_CHECKPOINT_ID}} if record.PARENT_CHECKPOINT_ID else None,
                    pending_writes=[]
                )
        except Exception as e:
            print(f"Checkpointer List Error: {str(e)}")
            return iter([])
