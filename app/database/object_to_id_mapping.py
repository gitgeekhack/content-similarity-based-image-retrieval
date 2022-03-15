# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# importing required configurations
from .db_connection_manager import DatabaseConnection
from app.constant import PANOPTIC_CLASSES

# object for database activities
db_obj = DatabaseConnection()


# function for mapping string object names to numeric id
def create_numeric_id_mapping():
    es = db_obj.connect()  # # connecting to database
    es.indices.create(index="object_id_mapping")  # creating index

    for class_ in PANOPTIC_CLASSES:
        es.index(index="object_id_mapping",
                 id=PANOPTIC_CLASSES.index(class_),
                 document={"obj_name": class_})  # inserting into index

    db_obj.close()  # closing database connection
