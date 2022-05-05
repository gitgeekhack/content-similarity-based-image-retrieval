# importing required libraries
import faiss
import app
from app.service.helper.generate_feature_vectors import FeatureExtraction
from app.database.db_helper import vector_already_present, store_not_indexed
from app.constant import SAVED_INDEX_FOLDER, DIMENSION
import numpy as np

vector_obj = FeatureExtraction()  # object for generating vectors

# crete faiss index if not present else read from storage
try:
    faiss_index = faiss.read_index(SAVED_INDEX_FOLDER + '/file.index')
except Exception as e:
    app.logger.info("Creating Faiss index")
    faiss_index = faiss.IndexFlatIP(DIMENSION)


def indexing(files):
    all_vectors = vector_obj.getvectors(files)  # generating all vectors

    not_present_vectors, ids = vector_already_present(all_vectors)  # finding vectors which is not present in index

    if not_present_vectors:
        numpy_vectors = np.array(not_present_vectors, dtype='float32')  # converting vector to 'float32' datatype

        faiss.normalize_L2(numpy_vectors)  # normalizing vectors
        if not faiss_index.is_trained:
            faiss_index.train(numpy_vectors)  # training faiss index
        faiss_index.add(numpy_vectors)  # adding vectors to faiss index
        faiss.write_index(faiss_index, SAVED_INDEX_FOLDER+'/file.index')  # saving faiss index to storage

        store_not_indexed(files, all_vectors, ids)  # storing vectors to database

    return len(not_present_vectors)


