import tensorflow as tf
import numpy as np
import time
import glob
import os.path
from app.constant import MODULE

class FeatureExtraction:
    def load_img(self, image_path):
        # Reads the image file and returns data type of string
        img = tf.io.read_file(image_path)

        # Decodes the image to W x H x 3 shape tensor with type of uint8
        img = tf.io.decode_jpeg(img, channels=3)

        # Resize the image to 224 x 244 x 3 shape tensor
        img = tf.image.resize_with_pad(img, 224, 224)

        # Converts the data type of uint8 to float32 by adding a new axis
        # This makes the img 1 x 224 x 224 x 3 tensor with the data type of float32
        # This is required for the mobilenet model we are using
        img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

        return img


    def single_image_vector(self, filename):
        img = self.load_img(filename)

        # Calculate the image feature vector of the img
        features = MODULE(img)

        # Remove single-dimensional entries from the 'features' array
        return np.squeeze(features)

    def save_image_vector(self, filename, feature_vector):
        outfile_name = os.path.basename(filename).split('.')[0] + ".npz"
        out_path = os.path.join('/home/nirav/PycharmProjects/Imagesimilarity_faiss/vectors', outfile_name)

        # Saves the 'feature_set' to a text file
        np.savetxt(out_path, feature_vector, delimiter=',')

    def getvectors(self, filenames):
        # Definition of module with using tfhub.dev handle
        print("----- Generating Feature Vectors -----")

        starttime = time.time()
        # Loops through all images in a local folder
        for filename in filenames:  # assuming gif
            feature_vector = self.single_image_vector(filename)

            self.save_image_vector(filename, feature_vector)

        print("Time taken to generate feature vectors : %f seconds"%(time.time() - starttime))
