from .db_connection_manager import DatabaseConnection
import json

db_obj = DatabaseConnection()


def vector_already_present(vectors):
    es = db_obj.connect()  # connecting to database
    try:
        es.indices.create(index="vector_mapping")
    except:
        pass
    not_present = []

    for vector in vectors:
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
        else:
            not_present.append(vector)

    db_obj.close(es)

    return not_present


# def store_not_indexed(files, not_present_vectors):
#     es = db_obj.connect()  # connecting to database
#
#     total_indexed = es.count(index="vector_mapping")['count']
#     for i, file in zip(files):
#         doc = {
#             "imagename": file
#         }
#         es.index(index="vector_mapping", document=doc, id=total_indexed+i)
#
#     db_obj.close(es)


def store_not_indexed(files, vectors):
    es = db_obj.connect()  # connecting to database
    try:
        es.indices.create(index="vector_mapping")
    except:
        pass
    total_indexed = es.count(index="vector_mapping")['count']
    for file, vector in zip(files, vectors):
        doc = {
            "imagename": file,
            "vector": vector
        }
        es.index(index="vector_mapping", document=doc, id=total_indexed+files.index(file))

    db_obj.close(es)

