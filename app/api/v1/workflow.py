from fastapi import APIRouter, Depends, Request, HTTPException, Response

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workflow import WorkflowCreate
from app.models.workflow import Workflow, create_workflow, get_workflow_by_id
from app.middleware.auth import get_current_user_from_cookie

# from app.crud.workflow import create_workflow, get_workflow_by_id
# from app.schemas.workflow import WorkflowCreate, WorkflowResponse

router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post(
    "/create",
)
def create_workflow_endpoint(
    data: WorkflowCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_from_cookie),
):
    try:
        workflow = create_workflow(
            session=db,
            name=data.name,
            description=data.description,
            created_by=data.created_by,
        )

        if workflow.created_by != user["user_id"]:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to create workflow for another user",
            )
        return {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "status": workflow.status,
            "created_at": workflow.created_at,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/get_workflow_by_user",
)


def get_workflow_by_user_endpoint(
    db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)
):
    print(user)
    try:
        print(user)
        workflows = (
            db.query(Workflow).filter(Workflow.created_by == user["user_id"]).all()
        )
        return [
            {
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "status": workflow.status,
                "created_at": workflow.created_at,
            }
            for workflow in workflows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{workflow_id}",
)
def get_workflow_endpoint(
    workflow_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_from_cookie),
):
    try:
        workflow = get_workflow_by_id(session=db, workflow_id=workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        if workflow.created_by != user["user_id"]:
            raise HTTPException(
                status_code=403, detail="Not authorized to view this workflow"
            )
        return {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "status": workflow.status,
            "created_at": workflow.created_at,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
