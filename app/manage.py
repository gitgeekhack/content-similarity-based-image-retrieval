import os
from flask import Flask
from app import config
from elasticsearch import Elasticsearch


def create_flask_app():
    app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)) + '/service/helper/Flask/templates')

    app.secret_key = "secret key"
    app.env = config.Environment.ENV
    return app


def create_database_connection():
    es = Elasticsearch(config.Database.HOST, basic_auth=(config.Database.USERNAME, config.Database.PASSWORD),
                       verify_certs=False)  # connecting to database using username and password
    return es
