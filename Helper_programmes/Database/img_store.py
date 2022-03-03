# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# importing Elasticsearch
from elasticsearch import Elasticsearch

# global variable 'es'
es=None

# function for connection to Elasticsearch database running on local system
def connect_to_db():
    global es
    es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "eNCL=VuBQL7UV6QpJxWe"), verify_certs=False) # connecting to database using username and password

# function for creating index if not exists
def create_index():
    global es
    try:
        es.indices.create(index="images")
    except:
        pass

# converting object names to numeric id defined in 'object_id_mapping' index
def convert_to_id(objects):
    global es
    converted_objects=[]
    for i in objects:
        response = es.search(index="object_id_mapping", body={"query":{"match":{"obj_name":i}}})
        converted_objects.append(int(response['hits']['hits'][0]['_id']))

    return converted_objects

# main function to store input image into database
def store_to_db(imgpath, objects):
    global es
    connect_to_db()
    create_index()

    doc={
        "imgpath":imgpath,
        "detected_objects":convert_to_id(objects)
    }
    es.index(index="images", document=doc) # inserting data
    es.close() # closing database connection










