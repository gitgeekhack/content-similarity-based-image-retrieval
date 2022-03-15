# importing required libraries
import os
from flask import Flask

# importing helper programmes
from app.common.utils import setup_logger, read_properties_file
from app.config import CONFIG
from app.constant import UPLOAD_FOLDER, SECRET_KEY, APP_ROOT
from app.database.db_connection_manager import DatabaseConnection
from app.database.object_to_id_mapping import create_numeric_id_mapping

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

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create if folder not exists
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # setting upload folder of application

    es = db_obj.connect()  # connecting to database
    # create index if not exists
    try:
        es.indices.create(index="images")
        create_numeric_id_mapping()  # creating mapping of object names to numeric id
    except:
        pass
    db_obj.close(es)  # closing database connection

    logger = setup_logger()
    app.logger.info('Starting [{}] server'.format(app.config['ENVIRONMENT']))
    return app, logger
