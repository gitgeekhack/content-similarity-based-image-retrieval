# importing helper programmes
from app.service.helper import indexer, searcher
from app.common.utils import MonoState


# Image indexer
class ImageIndexer(MonoState):
    def indeximages(self, imagepaths):
        image_indexed_count = indexer.indexing(imagepaths)  # image indexing
        return image_indexed_count


# Image searcher
class ImageSearcher(MonoState):
    def searchimages(self, imagepath):
        similar_images = searcher.searching(imagepath)  # image searching
        return similar_images

