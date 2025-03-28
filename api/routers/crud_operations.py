from typing import List

from fastapi import APIRouter, Query, Response
from starlette import status

from api.response_model import Task
from database.db_connect import add_task, update_task, update_status, delete_tasks, fetch_data, fetch_data_id

router = APIRouter()

@router.get(path="/task", tags=["Task"])
def fetch_task(response: Response):
    data = fetch_data()
    if data or data == []:
        response.status_code = status.HTTP_200_OK
        return data
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": {"Internal server error!"}}

@router.get(path="/task/{id}", tags=["Task"])
def fetch_task(response: Response, id: int):
    data = fetch_data_id(id)
    if data or data == []:
        response.status_code = status.HTTP_200_OK
        return data
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": {"Internal server error!"}}

@router.post(path="/task", tags=["Task"])
def create_task(response: Response, task: Task):
    success = add_task(task)
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"Status": "Success"}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": "Failed"}

@router.put(path="/task", tags=["Task"])
def modify_task(response: Response, id: int, task: Task):
    success = update_task(id, task)
    if success == 'Forbidden':
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"Status": "Forbidden status, insert 'done', 'in progress' or 'to do'"}
    elif success:
        response.status_code = status.HTTP_201_CREATED
        return {"Status": "Success"}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": "Failed"}

@router.put(path="/task/{id}", tags=["Task"])
def modify_status(response: Response, id: int, task_status: str):
    success = update_status(id, task_status)
    if success:
        response.status_code = status.HTTP_200_OK
        return {"Status": f"Status for {id} updated to {task_status}."}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": "Failed to update status"}

@router.delete(path="/task", tags=["Task"])
def delete_task(response: Response, id: int = Query(None, description="Id to delete")):
    success = delete_tasks(id)
    if success:
        response.status_code = status.HTTP_200_OK
        return {"Status": f"Successfully deleted tasks."}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Status": "Failed to delete."}