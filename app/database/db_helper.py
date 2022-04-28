# importing required libraries
from .db_connection_manager import DatabaseConnection
import json

db_obj = DatabaseConnection()  # object for connecting and closing database connection


# checking vector already present or not
def vector_already_present(vectors):
    es = db_obj.connect()

    not_present = []
    ids = []

    for j, vector in enumerate(vectors):
        str1 = '{"query": {"bool": {"must": ['
        for i in vector:
            str1 += '{{"match": {{"vector": {id} }}}},'.format(id=i)
        str2 = ']}}}'

        final_str = str1[:-1] + str2  # final query string

        query_string = json.loads(final_str)
        response = es.search(index="vector_mapping", body=query_string)

        if response['hits']['max_score']:
            if int(response['hits']['max_score']) != 1792:
                not_present.append(vector)
                ids.append(j)
        else:
            not_present.append(vector)
            ids.append(j)
    db_obj.close(es)

    return not_present, ids


# get imagename by id using database
def get_imagename_by_id(ids):
    es = db_obj.connect()

    imagenames = []
    for i in ids:
        if i != -1:
            response = es.get(index="vector_mapping", id=i)
            imagenames.append(response['_source']['imagename'])

    db_obj.close(es)
    return imagenames


# storing vectors to database
def store_not_indexed(files, vectors, ids):
    es = db_obj.connect()

    total_indexed = es.count(index="vector_mapping")['count']

    for id in ids:
        doc = {
            "imagename": files[id],
            "vector": vectors[id]
        }
        es.index(index="vector_mapping", document=doc, id=total_indexed+ids.index(id))

    db_obj.close(es)

