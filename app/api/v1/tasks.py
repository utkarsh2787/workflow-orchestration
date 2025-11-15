from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.db.session import get_db
from app.middleware.auth import get_current_user_from_cookie
from app.models.task import create_task, del_task_wk_id
from app.models.workflow import get_workflow_by_id
from app.schemas.task import TaskCreate


router = APIRouter(prefix="/task", tags=["tasks"])


@router.post("/add_task")
def add_tasks(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_from_cookie),
):
    workflow = get_workflow_by_id(db, data.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.created_by != user["user_id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to add tasks to this workflow"
        )
    task = create_task(
        db,
        name=data.name,
        command="",
        order=data.order,
        workflow_id=data.workflow_id,
        type=data.taskType,
        config=data.config,
        inputs=data.inputs,
        outputs=data,
        output_schema=data.output_schema,
    )
    return {"msg": "Task created successfully", "task_id": task.id}


@router.post("/add_tasks_bulk")
def add_tasks_bulk(
    data: list[TaskCreate],
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_from_cookie),
):
    created_task_ids = []
    del_task_wk_id(db, data[0].workflow_id)
    for task_data in data:
        workflow = get_workflow_by_id(db, task_data.workflow_id)
        if not workflow:
            raise HTTPException(
                status_code=404,
                detail=f"Workflow with id {task_data.workflow_id} not found",
            )
        if workflow.created_by != user["user_id"]:
            raise HTTPException(
                status_code=403, detail="Not authorized to add tasks to this workflow"
            )
        task = create_task(
            db,
            name=task_data.name,
            command="",
            order=task_data.order,
            workflow_id=task_data.workflow_id,
            type=task_data.taskType,
            config=task_data.config,
            inputs=task_data.inputs,
            output_schema=task_data.output_schema,
        )
        created_task_ids.append(task.id)
    return {"msg": "Tasks created successfully", "task_ids": created_task_ids}

