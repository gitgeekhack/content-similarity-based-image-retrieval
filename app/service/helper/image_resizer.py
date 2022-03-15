# importing libraries
import cv2
from enum import IntEnum

scale_factor = None  # global variable


class ImgHeight(IntEnum):
    low = 0
    medium = 1
    high = 2
    very_high = 3


# different functions to set 'scale_factor' according to height of an image
def height_very_high():
    global scale_factor
    scale_factor = 0.2

def height_high():
    global scale_factor
    scale_factor = 0.4

def height_medium():
    global scale_factor
    scale_factor = 0.6

def height_low():
    global scale_factor
    scale_factor = 0.8

handlers = {
    ImgHeight.low.value: height_low,
    ImgHeight.medium.value: height_medium,
    ImgHeight.high.value: height_high,
    ImgHeight.very_high.value: height_very_high
}


# setting 'scale_factor' using handlers
def handle_scale_factor(status):
    global scale_factor
    if status not in handlers:
        scale_factor = 0.1
    else:
        handler = handlers[status]
        handler()


# Function for resizing image
def image_resize(image):
    global scale_factor
    height = image.shape[0]
    width = image.shape[1]

    handle_scale_factor(height // 1000)

    # We are using scale_factor so input and output image will be of same aspect ratio
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    new_dimensions = (new_width, new_height)
    image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_LINEAR)

    return image
