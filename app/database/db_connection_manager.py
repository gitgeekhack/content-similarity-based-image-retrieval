# imporing required libraries
from elasticsearch import Elasticsearch
from app.config import DevelopmentConfig, ProductionConfig
import os
from app.common.utils import read_properties_file
from app.constant import APP_ROOT


# class for database connection activities
class DatabaseConnection:
    # function for connecting to database
    def connect(self):
        config = read_properties_file(os.path.join(APP_ROOT, "environment.properties"))
        config_name = os.getenv('APPLICATION_ENVIRONMENT', config['environment'])
        if config_name=='Development':
            es = Elasticsearch(DevelopmentConfig.HOST,
                           basic_auth=(DevelopmentConfig.USERNAME, DevelopmentConfig.PASSWORD),
                           verify_certs=False)
        else:
            es = Elasticsearch(ProductionConfig.HOST,
                               basic_auth=(ProductionConfig.USERNAME, ProductionConfig.PASSWORD),
                               verify_certs=False)
        return es

    # function for closing database connection
    def close(self, es):
        es.close()
