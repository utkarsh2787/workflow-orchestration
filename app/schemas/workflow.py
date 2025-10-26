from pydantic import BaseModel

class WorkflowCreate(BaseModel):
    name: str
    description: str
    created_by: int | None = None