# importing required images
import faiss
import numpy as np
import app
from app.service.helper.generate_feature_vectors import FeatureExtraction
from app.constant import SAVED_INDEX_FOLDER
from app.service.helper import indexer
from app.database.helper import DatabaseHelper
from app.constant import NO_OF_NEIGHBORS, DISTANCE_THRESHOLD

vector_obj = FeatureExtraction()  # object for generating vectors

db = DatabaseHelper()

def searching(imagepath, range_search):
    # read index if available else give error message
    try:
        faiss_index = faiss.read_index(SAVED_INDEX_FOLDER+'/file.index')
    except Exception as e:
        app.logger.warning("Error in loading index", e)
        return 'No index'

    all_vectors = vector_obj.getvectors(imagepath)  # generating all vectors
    numpy_vectors = np.array(all_vectors, dtype='float32')
    faiss.normalize_L2(numpy_vectors)  # normalizing vectors
    if range_search:  # to search with distance threshold
        _, distances, indexes = faiss_index.range_search(numpy_vectors, DISTANCE_THRESHOLD)  # searching similar images

        # sorting indexes by distance
        similar_indexes = [indexes[list(distances).index(i)] for i in sorted(distances, reverse=True)]
    else:  # to search with no. of neighbors
        distances, indexes = faiss_index.search(numpy_vectors, NO_OF_NEIGHBORS)  # searching similar images

        # filtering images by threshold
        similar_indexes = [indexes[0][i] for i, distance in enumerate(distances[0]) if distance >= DISTANCE_THRESHOLD]
    indexer.indexing(imagepath)  # adding search image to faiss index
    return db.get_imagename_by_id(similar_indexes)  # returning imagenames by using indexes returned by search

