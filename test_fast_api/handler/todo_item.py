from datetime import datetime
from typing import List

from pydantic import BaseModel
from fastapi import Query
from fastapi import HTTPException

from test_fast_api.app import app
from test_fast_api.handler.todo_list import TODO_LIST_RESOURCE, TODO_LIST_RESOURCE_ID, get_todo_list
from test_fast_api.model import todo_model


TODO_ITEM_RESOURCE = f'{TODO_LIST_RESOURCE}/{TODO_LIST_RESOURCE_ID}/item'
TODO_ITEM_RESOURCE_ID = '{item_id}'


class TodoItemResource(BaseModel):
    text: str = Query(
        '',
        min_length=0,
        max_length=1024,
        description="Text"
    )
    due_date: datetime = None
    finished_status: bool = Query(False, description="Finished status")


class TodoItemResponse(TodoItemResource):
    id: str


@app.post(TODO_ITEM_RESOURCE, status_code=201, response_model=TodoItemResponse)
def create_todo_item(todo_list_id: str, resource: TodoItemResource):
    todo_list = get_todo_list(todo_list_id)
    todo_item = todo_model.TodoItemModel(todo_list=todo_list, **resource.dict())
    todo_item.save()
    return todo_item.to_dict()


@app.put(f'{TODO_ITEM_RESOURCE}/{TODO_ITEM_RESOURCE_ID}', response_model=TodoItemResponse)
def modify_todo_item(todo_list_id: str, item_id: str, resource: TodoItemResource):
    todo_list = get_todo_list(todo_list_id)
    todo_item = todo_model.TodoItemModel.objects(pk=item_id, todo_list=todo_list).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_item.update(**resource.dict())
    return todo_item.to_dict()


@app.get(f'{TODO_ITEM_RESOURCE}/{TODO_ITEM_RESOURCE_ID}', response_model=TodoItemResponse)
def get_todo_items(todo_list_id: str, item_id: str):
    todo_list = get_todo_list(todo_list_id)
    todo_item = todo_model.TodoItemModel.objects(pk=item_id, todo_list=todo_list).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return todo_item.to_dict()


@app.get(TODO_ITEM_RESOURCE, response_model=List[TodoItemResponse])
def list_todo_items(todo_list_id: str):
    todo_list = get_todo_list(todo_list_id)
    todo_items = todo_model.TodoItemModel.objects(todo_list=todo_list).all()
    return [row.to_dict() for row in todo_items]


@app.delete(f'{TODO_ITEM_RESOURCE}/{TODO_ITEM_RESOURCE_ID}', status_code=204)
def delete_todo_item(todo_list_id: str, item_id: str):
    todo_list = get_todo_list(todo_list_id)
    todo_item = todo_model.TodoItemModel.objects(pk=item_id, todo_list=todo_list).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_item.delete()
