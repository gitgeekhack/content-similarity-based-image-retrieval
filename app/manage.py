import os.path
from flask import Flask
from app import config
from elasticsearch import Elasticsearch
#
# print(os.path.dirname(os.path.abspath(__file__)) + '/service/helper/Flask/templates')
# print(os.path.join(os.path.dirname(os.path.abspath(__file__)), '/service/helper/Flask/templates'))
def create_flask_app():
    app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)) + '/service/helper/Flask/templates')

    app.secret_key = "secret key"
    app.env = config.DevelopmentConfig.ENV
    return app


def create_database_connection():
    es = Elasticsearch(config.LocalDatabase.HOST, basic_auth=(config.LocalDatabase.USERNAME, config.LocalDatabase.PASSWORD),
                       verify_certs=False)  # connecting to database using username and password
    return es
