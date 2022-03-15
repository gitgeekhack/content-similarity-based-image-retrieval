# importing required libraries
import json
from .db_connection_manager import DatabaseConnection
from app.common.utils import object_to_key_map

# object for database activities
db_obj = DatabaseConnection()


# function for retrieving images by search keyword
def retrieve_by_single_object(searchkey):
    es = db_obj.connect()  # connecting to database

    # getting numeric key using search keyword
    mapped_key = object_to_key_map(es, searchkey)

    # retrieving images based on numeric key
    response = es.search(index="images", body={"query":{"match":{"detected_objects":mapped_key}}})
    images_with_searchkey = []
    for i in response['hits']['hits']:
        images_with_searchkey.append(i['_source']['imgpath'])

    db_obj.close(es)  # closing database connection

    return images_with_searchkey


# function for retrieving images which contains all objects of input image
def retrieve_by_multiple_objects(objects):
    es = db_obj.connect()  # connecting to database

    # convert object names from string to numeric id
    mapped_keys = []
    for object in objects:
        mapped_keys.append(object_to_key_map(es, object))

    # creating query string for retrieving images with all objects
    str1= '{"query": {"bool": {"must": ['
    for i in mapped_keys:
        str1 += '{{"match": {{"detected_objects": {id} }}}},'.format(id=i)
    str2 = ']}}}'
    
    final_str = str1[:-1] + str2 # final query string
    
    # Elasticsearch.search() function requires query as 'dict' object 
    # converting 'str' to 'dict' object
    query_string = json.loads(final_str)
    response = es.search(index="images", body=query_string)  # query for searching images from database

    # storing images into list using response object
    images_with_objects = []
    for i in response['hits']['hits']:
        images_with_objects.append(i['_source']['imgpath'])

    db_obj.close(es)  # closing database connection

    return images_with_objects
