import requests


def test_create_todo_list(todo_list):
    json = todo_list.json()
    assert json['name'] == 'home work'
    assert json['description'] == 'My home work todo list'
    assert 'id' in json


def test_fetch_todo_list(todo_list, service_url):
    todo_list_id = todo_list.json()['id']
    resp = requests.get(f'{service_url}/todo-list/{todo_list_id}')
    assert resp.status_code == 200
    assert resp.json() == todo_list.json()


def test_update_todo_list(todo_list, service_url):
    todo_list_id = todo_list.json()['id']
    resp_before = requests.get(f'{service_url}/todo-list/{todo_list_id}')
    assert resp_before.status_code == 200
    resp = requests.put(f'{service_url}/todo-list/{todo_list_id}', json={
        'name': 'fun work',
        'description': 'Fun work todo list'
    })
    assert resp.status_code == 200
    resp_after = requests.get(f'{service_url}/todo-list/{todo_list_id}')
    assert resp_after.status_code == 200
    assert resp_after.json()['name'] == 'fun work'
    assert resp_after.json()['description'] == 'Fun work todo list'


def test_list_todo_lists(todo_list, service_url):
    resp = requests.get(f'{service_url}/todo-list')
    assert resp.status_code == 200
    assert type(resp.json()) == list
    assert todo_list.json() in resp.json()
