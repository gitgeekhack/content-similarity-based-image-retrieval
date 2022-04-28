# importing required images
import faiss
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
    similar_indexes = []
    if range_search:  # to search with distance threshold
        _, distances, indexes = faiss_index.range_search(vector[0].reshape(1, -1), DISTANCE_THRESHOLD)
        similar_indexes = indexes
    else:  # to search with no. of neighbors
        distances, indexes = faiss_index.search(vector[0].reshape(1, -1), NO_OF_NEIGHBORS)  # searching similar images
        similar_indexes = indexes[0]
    indexer.indexing(imagepath)  # adding search image to faiss index
    return get_imagename_by_id(similar_indexes)  # returning imagenames by using indexes returned by search

