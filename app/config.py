CONFIG = {
    "Production": "app.config.ProductionConfig",
    "Staging": "app.config.StagingConfig",
    "Development": "app.config.DevelopmentConfig",
    "LocalDatabase": "app.config.LocalDatabaseConfig",
    "RemoteDatabase": "app.config.RemoteDatabaseConfig"
}


class BaseConfig(object):
    APP_NAME = 'Content-Based-Image-Retrieval'
    APP_VERSION = '1.0'


class DevelopmentConfig(BaseConfig):
    ENVIRONMENT = 'Development'


class StagingConfig(BaseConfig):
    ENVIRONMENT = 'Staging'


class ProductionConfig(BaseConfig):
    ENVIRONMENT = 'Production'


class LocalDatabaseConfig(BaseConfig):
    HOST = "https://localhost:9200"
    USERNAME = "elastic"
    PASSWORD = "eNCL=VuBQL7UV6QpJxWe"


class RemoteDatabaseConfig(BaseConfig):
    HOST = "set remote address here"
    USERNAME = "username"
    PASSWORD = "password"
