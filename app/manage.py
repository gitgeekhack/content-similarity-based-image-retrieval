# importing required libraries
import os
from flask import Flask

# importing helper programmes
from app.common.utils import setup_logger, read_properties_file
from app.config import CONFIG
from app.constant import UPLOAD_FOLDER, SAVED_INDEX_FOLDER, SECRET_KEY, APP_ROOT
from app.database.connection_manager import DatabaseConnection


# object for database activities
db_obj = DatabaseConnection()


# function for creating flask app
def create_app(debug=False):
    app = Flask(__name__, template_folder="./templates", static_folder="./static")
    app.debug = debug
    app.secret_key = SECRET_KEY
    config = read_properties_file(os.path.join(APP_ROOT, "environment.properties"))
    config_name = os.getenv('FLASK_CONFIGURATION', config['environment'])
    app.config.from_object(CONFIG[config_name])

    # create required folders if not exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(SAVED_INDEX_FOLDER, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # setting upload folder of application

    es = db_obj.connect()  # connecting to database

    # create elasticsearch index if not exists
    try:
        es.indices.create(index="vector_mapping")
    except Exception as e:
        app.logger.warning('Index already present', e)

    db_obj.close(es)  # closing database connection

    logger = setup_logger()
    app.logger.info('Starting [{}] server'.format(app.config['ENVIRONMENT']))
    return app, logger
