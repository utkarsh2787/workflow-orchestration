from pydantic import BaseModel
from sqlalchemy import JSON
from typing import Any, Dict, Optional


class TaskCreate(BaseModel):
    name: str
    workflow_id: int
    inputs: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    taskType: str
    order: int
    output_schema: Optional[Dict[str, Any]] = None
