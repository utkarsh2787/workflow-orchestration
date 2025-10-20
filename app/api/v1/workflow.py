from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workflow import WorkflowCreate
# from app.crud.workflow import create_workflow, get_workflow_by_id
# from app.schemas.workflow import WorkflowCreate, WorkflowResponse

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/",)
def create_workflow_endpoint(data:WorkflowCreate, db: Session = Depends(get_db)):
    print(data)
    return 'create_workflow(db, data)'

@router.get("/{workflow_id}",)
def get_workflow_endpoint(workflow_id: int, db: Session = Depends(get_db)):
    return f'get_workflow_by_id(db, {workflow_id})'
