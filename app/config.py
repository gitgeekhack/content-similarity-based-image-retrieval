# importing required libraries
import os
from dotenv import load_dotenv
load_dotenv()  # function to load environment variables


# Environment Configuration
class Environment(object):
    if os.environ['ENVIRONMENT'] == 'development':
        ENV = 'development'
    else:
        ENV = 'production'


# Database Configuration
class Database(object):
    if os.environ['DATABASE'] == 'local':
        HOST = "https://localhost:9200"
        USERNAME = "elastic"
        PASSWORD = "eNCL=VuBQL7UV6QpJxWe"
    else:
        HOST = "set remote address here"
        USERNAME = "username"
        PASSWORD = "password"
