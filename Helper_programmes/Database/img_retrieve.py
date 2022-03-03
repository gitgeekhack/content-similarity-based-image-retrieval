# importing Elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "eNCL=VuBQL7UV6QpJxWe"), verify_certs=False) # connecting to database using username and password

# function for retrieving images by search keyword
def image_retrieve(searchkey):
    # getting numeric key using search keyword
    response1 = es.search(index="object_id_mapping", body={"query":{"match":{"obj_name":searchkey}}})
    mapped_key = response1['hits']['hits'][0]['_id']

    # retrieving images based on numeric key
    response2 = es.search(index="images", body={"query":{"match":{"detected_objects":mapped_key}}})
    images_with_searchkey = []
    for i in response2['hits']['hits']:
        images_with_searchkey.append(i['_source']['imgpath'])

    es.close() # closing connection
    return images_with_searchkey
