# importing libraries
import cv2

# Function for resizing image
def image_resize(image):
    height = image.shape[0]
    width = image.shape[1]

    # Resizing image based on its size
    if height>3000:
        scale_factor = 0.2
    elif height>2000:
        scale_factor = 0.4
    elif height>1000:
        scale_factor = 0.6
    elif height>500:
        scale_factor = 0.8
    else:
        scale_factor = 1

    # We are using scale_factor so input and output image will be of same aspect ratio
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    new_dimensions = (new_width, new_height)
    image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_LINEAR)

    return image