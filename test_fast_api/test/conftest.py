import pytest
import yaml
import threading
import uvicorn
import os
import requests


@pytest.fixture(scope='session')
def config():
    config_path = os.environ.get('APP_CONFIG')
    with open(config_path, 'r') as stream:
        yield yaml.safe_load(stream)


@pytest.fixture(scope='session')
def service_url(request, config):
    server_config = config['server']
    yield f"http://{server_config['host']}:{server_config['port']}"


@pytest.fixture()
def todo_list(config, service_url):
    resp = requests.post(f'{service_url}/todo-list', json={
        'name': 'home work',
        'description': 'My home work todo list'
    })
    assert resp.status_code == 201
    yield resp
    resp = requests.delete(f'{service_url}/todo-list/{resp.json()["id"]}')
    assert resp.status_code == 204


@pytest.fixture()
def todo_item(config, service_url, todo_list):
    todo_list_id = todo_list.json()['id']
    resp = requests.post(f'{service_url}/todo-list/{todo_list_id}/item', json={
        'text': 'algebra',
    })
    assert resp.status_code == 201
    yield resp
    item_id = resp.json()["id"]
    resp = requests.delete(f'{service_url}/todo-list/{todo_list_id}/item/{item_id}')
    assert resp.status_code == 204
