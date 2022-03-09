# Filtering Warnings
import os
import warnings
warnings.filterwarnings('ignore')

from app.manage import create_database_connection
# importing Elasticsearch
from elasticsearch import Elasticsearch

es = create_database_connection()
# create index if not exists
try:
    es.indices.create(index="images")
except:
    pass

# function to store image into database
def store_to_db(imgpath, objects):
    # converting string object names into numeric ids
    converted_objects=[]
    for i in objects:
        response = es.search(index="object_id_mapping", body={"query":{"match":{"obj_name":i}}})
        converted_objects.append(int(response['hits']['hits'][0]['_id']))

    # inserting into database
    doc = {
        "imgpath": imgpath,
        "detected_objects": converted_objects
    }
    es.index(index="images", document=doc)


