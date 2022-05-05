import tensorflow as tf
import numpy as np
from app.common.utils import MonoState
import tensorflow_hub as hub

module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
module = hub.load(module_handle)


class FeatureExtraction(MonoState):

    # function for reading image from storage
    def load_img(self, image_path):
        img = tf.io.read_file(image_path)  # reading image

        # Decodes the image to W x H x 3 shape tensor with type of uint8
        img = tf.io.decode_jpeg(img, channels=3)

        # Resize the image to 224 x 244 x 3 shape tensor
        img = tf.image.resize_with_pad(img, 224, 224)

        # Converts the data type of uint8 to float32 by adding a new axis
        # This makes the img 1 x 224 x 224 x 3 tensor with the data type of float32
        # This is required for the mobilenet model we are using
        img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

        return img

    # function for generating vectors
    def getvectors(self, filenames):
        vectors = []
        for filename in filenames:
            img = self.load_img(filename)
            features = module(img)
            feature_vector = np.squeeze(features)
            vectors.append(feature_vector)
        return vectors
