# importing helper programmes
from Helper_programmes.Obj_detector import ObjDetection
from Helper_programmes.Database.img_store import store_to_db

imgpath = "/home/mtech/Downloads/input5.jpeg"

# object detection
obj = ObjDetection()
objects_detected = obj.predict(imgpath)
print(objects_detected)

# Storing into database
store_to_db(imgpath, objects_detected)
