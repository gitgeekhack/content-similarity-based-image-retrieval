import faiss
import time
from generate_feature_vectors import FeatureExtraction
from app.constant import APP_ROOT

obj = FeatureExtraction()

try:
    index = faiss.read_index(APP_ROOT + '/data/SavedIndex/file.index')
except:
    print('Index not available')


class SearchSimilarImages:
    def search(self, imagepath):
        vector = obj.single_image_vector(imagepath)
        t = time.time()
        distance, indx = index.search(vector.reshape(1, -1), 5)
        print('time taken to search:', time.time()-t)

        print(indx)

