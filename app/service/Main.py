# importing helper programmes
from app.service.helper import Object_detection
from app.database.image_store import store_to_db
from app.database.image_retrieve import retrieve_by_multiple_objects


# object detection on image
class ObjectDetector:
    def detect(self, imgpath):
        objects_detected = Object_detection.predict(imgpath)
        return objects_detected


# storing image to database
class StoreImage:
    def store(self, imgpath, objects_detected):
        store_to_db(imgpath, objects_detected)  # Storing into database


# retrieving images from database
class RetrieveImages:
    def retrieve(self, objects_list):
        images_returned = retrieve_by_multiple_objects(objects_list)
        return images_returned