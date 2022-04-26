import os
import faiss
from app.service.helper.generate_feature_vectors import FeatureExtraction
from app.database.store import vector_already_present, store_not_indexed
from app.constant import APP_ROOT
import numpy as np
import glob

obj = FeatureExtraction()

no_of_vectors = len(os.listdir(APP_ROOT + "/data/Vectors"))

try:
    faiss_index = faiss.read_index(APP_ROOT + '/data/SavedIndex/file.index')
except:
    quantizer = faiss.IndexFlatIP(1792)
    faiss_index = faiss.IndexIVFFlat(quantizer, 1792, int(np.sqrt(no_of_vectors)) + 1, faiss.METRIC_L2)


def Index(files):
    arr = obj.getvectors(files)

    not_present_vectors = vector_already_present(arr)

    if not_present_vectors:
        numpy_arr = np.array(not_present_vectors, dtype='float32')

        faiss.normalize_L2(numpy_arr)
        faiss_index.train(numpy_arr)
        faiss_index.add(numpy_arr)
        faiss.write_index(faiss_index, APP_ROOT+'/data/SavedIndex/file.index')

        store_not_indexed(files, not_present_vectors)


Index(glob.glob("/home/nirav/Desktop/Image/*.jpg"))

