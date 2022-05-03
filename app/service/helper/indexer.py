# importing required libraries
import faiss
import app
from app.service.helper.generate_feature_vectors import FeatureExtraction
from app.database.db_helper import vector_already_present, store_not_indexed
from app.database.db_connection_manager import DatabaseConnection
from app.constant import SAVED_INDEX_FOLDER, DIMENSION
import numpy as np

vector_obj = FeatureExtraction()  # object for generating vectors

db_obj = DatabaseConnection()  # object for database related operations

es = db_obj.connect()
total_indexed = es.count(index="vector_mapping")['count']  # finding no. of already indexed items
db_obj.close(es)

# crete faiss index if not present else read from storage
try:
    faiss_index = faiss.read_index(SAVED_INDEX_FOLDER + '/file.index')
except Exception as e:
    app.logger.info("Creating Faiss index")
    faiss_index = faiss.IndexFlatIP(DIMENSION)
    # faiss_index = faiss.IndexIVFFlat(quantizer, DIMENSION, int(np.sqrt(300)))


def indexing(files):
    arr = vector_obj.getvectors(files)  # generating all vectors

    not_present_vectors, ids = vector_already_present(arr)  # finding vectors which is not present in index

    if not_present_vectors:
        numpy_arr = np.array(not_present_vectors, dtype='float32')  # converting vector to 'float32' datatype

        faiss.normalize_L2(numpy_arr)  # normalizing array
        if not faiss_index.is_trained:
            faiss_index.train(numpy_arr)  # training faiss index
        faiss_index.add(numpy_arr)  # adding vectors to faiss index
        faiss.write_index(faiss_index, SAVED_INDEX_FOLDER+'/file.index')  # saving faiss index to storage

        store_not_indexed(files, arr, ids)  # storing vectors to database

    return len(not_present_vectors)


