import os
import yaml
import logging

from fastapi import FastAPI
import mongoengine


class FastApiApplication:
    def __init__(self):
        config_path = os.environ.get('APP_CONFIG')
        if config_path is None:
            raise Exception('Env variable "APP_CONFIG" must be specified')
        self.config = yaml.safe_load
        with open(config_path, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.exception('Cannot load config file.')
                raise
        self.db_client = mongoengine.connect(**self.config['db'])
        self.app = FastAPI()


fast_api_application = FastApiApplication()
app = fast_api_application.app


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.db_client.close()
