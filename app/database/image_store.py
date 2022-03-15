# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# importing required configurations
from .db_connection_manager import DatabaseConnection
from app.common.utils import object_to_key_map

# object for database activities
db_obj = DatabaseConnection()


# function to store image into database
def store_to_db(imgpath, objects):
    es = db_obj.connect()  # connecting to database
    # converting string object names into numeric ids
    converted_objects=[]
    for object in objects:
        converted_objects.append(object_to_key_map(es, object))

    # inserting into database
    doc = {
        "imgpath": imgpath,
        "detected_objects": converted_objects
    }
    es.index(index="images", document=doc)

    db_obj.close(es)  # closing database connection
