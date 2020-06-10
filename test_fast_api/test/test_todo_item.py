import requests


def test_create_todo_item(todo_item):
    json = todo_item.json()
    assert json['text'] == 'algebra'
    assert 'id' in json


def test_update_todo_item(todo_list, todo_item, service_url):
    todo_list_id = todo_list.json()['id']
    todo_item_id = todo_item.json()['id']
    resource_url = f'{service_url}/todo-list/{todo_list_id}/item/{todo_item_id}'
    resp_before = requests.get(resource_url)
    assert resp_before.status_code == 200
    resp = requests.put(resource_url, json={
        'text': 'algebra',
        'finished_status': True
    })
    assert resp.status_code == 200
    resp_after = requests.get(resource_url)
    assert resp_after.status_code == 200
    assert resp_after.json()['text'] == 'algebra'
    assert resp_after.json()['finished_status'] is True


def test_list_todo_items(todo_list, todo_item, service_url):
    todo_list_id = todo_list.json()['id']
    resp = requests.get(f'{service_url}/todo-list/{todo_list_id}/item')
    assert resp.status_code == 200
    assert type(resp.json()) == list
    assert todo_item.json() in resp.json()


def test_list_not_found_todo_items(todo_list, todo_item, service_url):
    todo_item_id = todo_item.json()['id']
    resource_url = f'{service_url}/todo-list/5ee0a777da77af30cfd1991a/item/{todo_item_id}'
    resp = requests.get(resource_url)
    assert resp.status_code == 404
