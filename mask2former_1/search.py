# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# using helper programmes
from Helper_programmes.Database.img_retrieve import single_key_retrieve, multiple_key_retrieve
from Helper_programmes.Obj_detector import ObjDetection

multiple = False # 'True' for multiple keys, 'False' for single key

if multiple:
    imgpath = "/home/mtech/Downloads/input2.png" # Enter your image path here
    obj = ObjDetection()
    objects_detected = obj.predict(imgpath)
    print(multiple_key_retrieve(objects_detected))
else:
    searchkey = input('Enter key you want to search: ')
    print(single_key_retrieve(searchkey)) # using function to retrieve images based on search key given by user