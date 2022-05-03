# importing required images
import faiss
import numpy as np
import app
from app.service.helper.generate_feature_vectors import FeatureExtraction
from app.constant import SAVED_INDEX_FOLDER
from app.service.helper import indexer
from app.database.db_helper import get_imagename_by_id
from app.constant import NO_OF_NEIGHBORS, DISTANCE_THRESHOLD

vector_obj = FeatureExtraction()  # object for generating vectors


def searching(imagepath, range_search):
    # read index if available else give error message
    try:
        faiss_index = faiss.read_index(SAVED_INDEX_FOLDER+'/file.index')
    except Exception as e:
        app.logger.warning("Error in loading index", e)
        return 'No index'

    vector = vector_obj.getvectors(imagepath)  # generating all vectors
    arr = np.array(vector, dtype='float32')
    faiss.normalize_L2(arr)
    similar_indexes = []
    if range_search:  # to search with distance threshold
        _, distances, indexes = faiss_index.range_search(arr, DISTANCE_THRESHOLD)
        similar_indexes = [indexes[list(distances).index(i)] for i in sorted(distances, reverse=True)]
    else:  # to search with no. of neighbors
        distances, indexes = faiss_index.search(arr, NO_OF_NEIGHBORS)  # searching similar images
        similar_indexes = indexes[0]
    indexer.indexing(imagepath)  # adding search image to faiss index
    return get_imagename_by_id(similar_indexes)  # returning imagenames by using indexes returned by search

