# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# using helper programmes
from Helper_programmes.Database.img_retrieve import single_key_retrieve, multiple_key_retrieve
from Helper_programmes.Obj_detector import ObjDetection

# Class for searching images based on either key or image
class ImageSearching:
    def __init__(self, multiple):
        self.is_multiple = multiple # 'True' for multiple keys, 'False' for single key

    # function to search images
    def search_images(self):
        if self.is_multiple:
            imgpath = "/home/mtech/Downloads/input1.jpg" # Enter your image path here
            obj = ObjDetection()
            objects_detected = obj.predict(imgpath)
            print(multiple_key_retrieve(objects_detected))
        else:
            searchkey = input('Enter key you want to search: ')
            print(single_key_retrieve(searchkey)) # using function to retrieve images based on search key given by user

obj_single = ImageSearching(False)
obj_multiple = ImageSearching(True)

obj_single.search_images()