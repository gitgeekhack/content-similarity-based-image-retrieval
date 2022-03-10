# importing required libraries
import os
from flask import Flask
from app import config
from elasticsearch import Elasticsearch


# function for creating flask app
def create_flask_app():
    app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)) + '/service/helper/Flask/templates')

    app.secret_key = "secret key"
    app.env = config.Environment.ENV # setting application environment
    return app


# function for connecting to elasticsearch database
def create_database_connection():
    es = Elasticsearch(config.Database.HOST, basic_auth=(config.Database.USERNAME, config.Database.PASSWORD),
                       verify_certs=False)  # connecting to database using username and password
    return es
