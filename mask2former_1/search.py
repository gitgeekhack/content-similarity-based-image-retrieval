# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# using helper programmes
from Helper_programmes.Database.img_retrieve import image_retrieve

searchkey = input('Enter key you want to search: ')
list_of_images = image_retrieve(searchkey) # using function to retrieve images based on search key given by user

print(list_of_images)