# Environment Configuration
import os


class Config(object):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'


# Database Configuration
class Database(object):
    HOST = None
    USERNAME = None
    PASSWORD = None


class LocalDatabase(Database):
    HOST = "https://localhost:9200"
    USERNAME = "elastic"
    PASSWORD = "eNCL=VuBQL7UV6QpJxWe"


class RemoteDatabase(Database):
    HOST = "set remote address here"
    USERNAME = "username"
    PASSWORD = "password"