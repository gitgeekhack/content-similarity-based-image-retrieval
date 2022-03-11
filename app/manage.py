# importing required libraries
import os
from elasticsearch import Elasticsearch
from flask import Flask

# importing helper programmes
from app.common.utils import setup_logger, read_properties_file
from app.config import CONFIG, LocalDatabaseConfig, RemoteDatabaseConfig


# function for creating flask app
def create_app(debug=False):
    app = Flask(__name__, template_folder="./templates")
    app.debug = debug
    app.secret_key = "wljsdlflsdkflskd"
    parent_dir = os.path.dirname(os.path.abspath(__file__))  # finding parent directory of file
    config = read_properties_file(os.path.join(parent_dir, "environment.properties"))
    config_name = os.getenv('FLASK_CONFIGURATION', config['environment'])
    app.config.from_object(CONFIG[config_name])

    UPLOAD_FOLDER = parent_dir + '/data/Uploaded_images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # setting upload folder of application
    logger = setup_logger()
    app.logger.info('Starting [{}] server'.format(app.config['ENVIRONMENT']))
    return app, logger


# function for connecting to elasticsearch database
def create_database_connection():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config = read_properties_file(os.path.join(parent_dir, "environment.properties"))
    config_name = os.getenv('DATABASE_CONFIGURATION', config['database'])

    # checking if database is local or remote
    if config_name == 'LocalDatabase':
        es = Elasticsearch(LocalDatabaseConfig.HOST,
                           basic_auth=(LocalDatabaseConfig.USERNAME, LocalDatabaseConfig.PASSWORD),
                           verify_certs=False)  # connecting to database using username and password
    else:
        es = Elasticsearch(RemoteDatabaseConfig.HOST,
                           basic_auth=(RemoteDatabaseConfig.USERNAME, RemoteDatabaseConfig.PASSWORD),
                           verify_certs=False)
    return es