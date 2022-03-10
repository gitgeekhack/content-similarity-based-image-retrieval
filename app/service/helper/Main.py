# importing helper programmes
from app.service.helper.Obj_detector import ObjDetection
from app.service.helper.Database.img_store import store_to_db


# object detection
def detect_objects(imgpath):
    obj = ObjDetection()
    objects_detected = obj.predict(imgpath)
    return objects_detected


# storing to database
def store_objects(imgpath, objects_detected):
    store_to_db(imgpath, objects_detected)  # Storing into database
