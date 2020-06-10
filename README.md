Test Fast API + Mongo DB


INSTALLATION
1. Install server
    $ pip install git+https://github.com/mhorban/test-fast-api
2. Prepare config file
    $ wget https://github.com/mhorban/test-fast-api/blob/master/test_fast_api/test/config/dev-config.yaml -P /tmp/test-fast-api/


RUN APPLICATION AND DB
1. Run the server:
    $ APP_CONFIG=/tmp/test-fast-api/dev-config.yaml uvicorn test_fast_api.app:app --port 9000
2. Run mongodb
    $ docker run -d -p 27017:27017 mongo


HOW TO USE
Application uses FastAPI lib so after starting service all documentation can be found at http://127.0.0.1:9000/docs
Examples:
- Create todo list
    $ curl -X POST http://127.0.0.1:9000/todo-list -v -d '{"name": "home work"}'
    $ curl -X POST http://127.0.0.1:9000/todo-list -v -d '{"name": "garden work", "description": ""}'
- Fetch todo list
    $ curl -X GET http://127.0.0.1:9000/todo-list/<ID> -v
- Modify todo list
    $ curl -X PUT http://127.0.0.1:9000/todo-list/<ID> -v -d '{"name": "home work", "description": "short descr"}'
- List todo lists
    $ curl -X GET http://127.0.0.1:9000/todo-list -v
- Delete todo list
    $ curl -X DELETE http://127.0.0.1:9000/todo-list/<ID> -v
- Add todo item
    $ curl -X POST http://127.0.0.1:9000/todo-list/<ID>/item -v -d '{"text": "math"}'
- Modify todo item
    $curl -X PUT http://127.0.0.1:9000/todo-list/<ID>/item/<ITEM_ID> -v -d '{"text": "cut branch DONOT FORGET!!!!!!"}'
- List todo items
    $ curl -X GET http://127.0.0.1:9000/todo-list/<ID>/item -v
- Delete todo item
    $ curl -X DELETE http://127.0.0.1:9000/todo-list/<ID>/item/<ITEM_ID> -v


RUN TESTS
First of all you need to RUN APPLICATION AND DB. Then execute commands:
    $ pip install -r test_fast_api/test/test_requirements.txt
    $ APP_CONFIG=/tmp/test-fast-api/dev-config.yaml pytest test_fast_api/test
