# importing required libraries
from elasticsearch import Elasticsearch
import json

es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "eNCL=VuBQL7UV6QpJxWe"), verify_certs=False) # connecting to database using username and password

# function for retrieving images by search keyword
def single_key_retrieve(searchkey):
    # getting numeric key using search keyword
    response1 = es.search(index="object_id_mapping", body={"query":{"match":{"obj_name":searchkey}}})
    mapped_key = response1['hits']['hits'][0]['_id']

    # retrieving images based on numeric key
    response2 = es.search(index="images", body={"query":{"match":{"detected_objects":mapped_key}}})
    images_with_searchkey = []
    for i in response2['hits']['hits']:
        images_with_searchkey.append(i['_source']['imgpath'])

    return images_with_searchkey


# function for retrieving images which contains all objects of input image
def multiple_key_retrieve(keys):
    # convert key names from string to numeric id
    mapped_keys = []
    for i in keys:
        res = es.search(index="object_id_mapping", body={"query":{"match":{"obj_name":i}}})
        mapped_keys.append(res['hits']['hits'][0]['_id'])

    # creating query string for retrieving images with all objects
    str1= '{"query": {"bool": {"must": ['
    for i in mapped_keys:
        str1 += '{{"match": {{"detected_objects": {id} }}}},'.format(id=i)
    str2 = ']}}}'
    
    final_str = str1[:-1] + str2 # final query string
    
    # Elasticsearch.search() function requires query as 'dict' object 
    # converting 'str' to 'dict' object
    query_string = json.loads(final_str)
    response = es.search(index="images", body=query_string)

    # storing images into list using response object
    images_with_searchkeys = []
    for i in response['hits']['hits']:
        images_with_searchkeys.append(i['_source']['imgpath'])

    return images_with_searchkeys

