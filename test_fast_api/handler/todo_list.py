from typing import List

from pydantic import BaseModel
from fastapi import Query
from fastapi import HTTPException

from test_fast_api.app import app
from test_fast_api.model import todo_model


TODO_LIST_RESOURCE = '/todo-list'
TODO_LIST_RESOURCE_ID = '{todo_list_id}'


class TodoListResource(BaseModel):
    name: str = Query(
        ...,
        min_length=1,
        max_length=128,
        description="Name of a todo list"
    )
    description: str = Query(
        None,
        min_length=0,
        max_length=1024,
        description="Todo list description")


class TodoListResponse(TodoListResource):
    id: str


@app.post(TODO_LIST_RESOURCE, status_code=201, response_model=TodoListResponse)
def create_todo_list(resource: TodoListResource):
    todo_list = todo_model.TodoListModel(**resource.dict())
    todo_list.save()
    return todo_list.to_dict()


def get_todo_list(todo_list_id: str):
    todo_list = todo_model.TodoListModel.objects(pk=todo_list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return todo_list


@app.get(f'{TODO_LIST_RESOURCE}/{TODO_LIST_RESOURCE_ID}', response_model=TodoListResponse)
def fetch_todo_list(todo_list_id: str):
    todo_list = get_todo_list(todo_list_id)
    return todo_list.to_dict()


@app.put(f'{TODO_LIST_RESOURCE}/{TODO_LIST_RESOURCE_ID}', response_model=TodoListResponse)
def modify_todo_list(todo_list_id: str, resource: TodoListResource):
    todo_list = get_todo_list(todo_list_id)
    todo_list.update(**resource.dict())
    return todo_list.to_dict()


@app.get(TODO_LIST_RESOURCE, response_model=List[TodoListResponse])
def list_todo_lists():
    todo_lists = todo_model.TodoListModel.objects().all()
    return [row.to_dict() for row in todo_lists]


@app.delete(f'{TODO_LIST_RESOURCE}/{TODO_LIST_RESOURCE_ID}', status_code=204)
def delete_todo_list(todo_list_id: str):
    todo_list = get_todo_list(todo_list_id)
    todo_list.delete()
