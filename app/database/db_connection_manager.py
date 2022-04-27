# imporing required libraries
from elasticsearch import Elasticsearch
import os
from app.common.utils import read_properties_file, MonoState, load_config
from app.constant import APP_ROOT
from app.config import CONFIG


# class for database connection activities
class DatabaseConnection(MonoState):
    # function for connecting to database
    def connect(self):
        config = read_properties_file(os.path.join(APP_ROOT, "environment.properties"))
        config_name = os.getenv('APPLICATION_ENVIRONMENT', config['environment'])
        config_environment = load_config(CONFIG[config_name])  # importing environment specific properties
        es = Elasticsearch(config_environment.HOST,
                           basic_auth=(config_environment.USERNAME, config_environment.PASSWORD), verify_certs=False)
        return es

    # function for closing database connection
    def close(self, es):
        es.close()
