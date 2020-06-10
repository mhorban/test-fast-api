import uvicorn

from test_fast_api.handler import todo_item
from test_fast_api.handler import todo_list
from test_fast_api.app import app, fast_api_application


def run():
    server_config = fast_api_application.config['server']
    uvicorn.run(app, host=server_config['host'], port=server_config['port'])


if __name__ == "__main__":
    run()
