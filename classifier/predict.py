# Using a TensorFlow Neural Network to predict where land is
# OLD NN: https://gist.github.com/WebCoder49/24a08fb35383cd5f92d58cef93470773
from copy import deepcopy

import cv2
import numpy as np

from results.camera_data import cam_cover_mask
from settings import CLASSIFIER_CERTAINTY_THRESHOLD as CERTAINTY_THRESHOLD
from settings import CLASSIFIER_TILE_SIZE as TILE_SIZE

"""Constants for cropping image to place in model"""
from settings import CLASSIFIER_CROP_SIZE as CROP_SIZE

import os

from tensorflow import keras

PIXELS_TO_CENTRE = CROP_SIZE // 2
PIXELS_TO_CENTRE_2 = CROP_SIZE - PIXELS_TO_CENTRE

MODEL = None


def load_model():
    global MODEL
    print("Loading model...")
    MODEL = keras.models.load_model(os.path.join("data", "classifier", "model"))
    print("Finished loading the model", MODEL)
    print(MODEL.summary())


class Classifier:
    """Using a TensorFlow Neural Network to predict where land is. Create a `Classifier`, then `predict_image` to get the land mask."""

    def __init__(self, channels):
        """Create a `Classifier`"""
        # Save channels
        self.nir, self.vis, self.ndvi = channels

        self.height = (
            self.vis.shape[0] // TILE_SIZE
        ) * TILE_SIZE  # Multiple of tile_size
        self.width = (
            self.vis.shape[1] // TILE_SIZE
        ) * TILE_SIZE  # Multiple of tile_size

    def get_crop(self, x: int, y: int):
        """Get the cropped portion of the image from nir, vis and ndvi"""
        # A "crop" is the neighbourhood of a pixel passed to the model as input
        start_y = y - PIXELS_TO_CENTRE
        end_y = y + PIXELS_TO_CENTRE_2
        start_x = x - PIXELS_TO_CENTRE
        end_x = x + PIXELS_TO_CENTRE_2

        height, width = self.vis.shape

        nir_crop = self.nir[start_y:end_y, start_x:end_x]
        vis_crop = self.vis[start_y:end_y, start_x:end_x]
        ndvi_crop = self.ndvi[start_y:end_y, start_x:end_x]

        if start_y < 0:
            for i in range(CROP_SIZE - nir_crop.shape[0]):
                empty_line = Classifier.create_empty_col(nir_crop.shape[1])  # Width
                nir_crop = np.vstack([empty_line, nir_crop])  # Vertical, before
                vis_crop = np.vstack([empty_line, vis_crop])  # Vertical, before
                ndvi_crop = np.vstack([empty_line, ndvi_crop])  # Vertical, before
            # print("-y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        elif end_y > height:
            for i in range(CROP_SIZE - nir_crop.shape[0]):
                empty_line = Classifier.create_empty_col(nir_crop.shape[1])  # Width
                nir_crop = np.vstack([nir_crop, empty_line])  # Vertical, after
                vis_crop = np.vstack([vis_crop, empty_line])  # Vertical, after
                ndvi_crop = np.vstack([ndvi_crop, empty_line])  # Vertical, after
            # print("+y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        if start_x < 0:
            for i in range(CROP_SIZE - nir_crop.shape[1]):
                empty_line = Classifier.create_empty_row(nir_crop.shape[0])  # Height
                nir_crop = np.hstack([empty_line, nir_crop])  # Horizontal, before
                vis_crop = np.hstack([empty_line, vis_crop])  # Horizontal, before
                ndvi_crop = np.hstack([empty_line, ndvi_crop])  # Horizontal, before
                # print(nir_crop)
            # print("-x>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        elif end_x > width:
            for i in range(CROP_SIZE - nir_crop.shape[1]):
                empty_line = Classifier.create_empty_row(nir_crop.shape[0])  # Height
                nir_crop = np.hstack([nir_crop, empty_line])  # Horizontal, after
                vis_crop = np.hstack([vis_crop, empty_line])  # Horizontal, after
                ndvi_crop = np.hstack([ndvi_crop, empty_line])  # Horizontal, after
            # print("+x>", nir_crop.shape, vis_crop.shape, start_x, start_y)

        return nir_crop.astype(float), vis_crop.astype(float), ndvi_crop.astype(float)

    def predict_image(self):
        """Return a mask of which pixels are land from the nir, vis and ndvi channels. If this is slow, update `settings."""
        crops = []

        where_useful = [] # Don't pass through NN - camera cover

        for y in range(0, self.height, TILE_SIZE):
            for x in range(0, self.width, TILE_SIZE):
                is_useful = (self.vis[y, x] > 0) and (self.nir[y, x] > 0) # Not camera cover / night; can pass through NN
                where_useful.append(is_useful)
                if is_useful:
                    # Not completely black
                    crop = cv2.merge(self.get_crop(x, y)) # Merge channels returned
                    # cv2_imshow(crop[1])
                    # print(x, y, nir[y, x], vis[y, x])
                    # cv2_imshow(crop[1])
                    crops.append(crop)



        crops = np.array(crops)
        if MODEL is None:
            load_model()
        print(MODEL)


        if len(crops) == 0:
            prediction = []
            print("NOTHING TO PREDICT")
        else:
            prediction = MODEL.predict(crops)

        # Add cover - 0 certainty at camera cover
        shaped_prediction = np.zeros(len(where_useful))
        shaped_prediction[where_useful] = np.reshape(prediction, (-1)) # 1D

        # Reshape into grid
        shaped_prediction = np.reshape(shaped_prediction, (self.height // TILE_SIZE, self.width // TILE_SIZE))  # grid
        shaped_prediction = cv2.resize(shaped_prediction, None, None, TILE_SIZE, TILE_SIZE, cv2.INTER_NEAREST)  # Nearest neighbour

        return self.prediction_to_mask(shaped_prediction)

    def prediction_to_mask(self, prediction):
        """Change float prediction certainty matrix to a boolean land mask"""

        return prediction > CERTAINTY_THRESHOLD


    @staticmethod
    def create_empty_col(length):
        """Padding for crops - Create a line of zeros all in a 1-item array of len length"""
        return np.zeros(length)

    @staticmethod
    def create_empty_row(length):
        """Padding for crops - Create a line of zeros each in a 1-item array of len length"""
        return np.array([np.array([0]) for x in range(length)])

    def crop_to_tiles(self, img):
        """Crop an image to make it the same shape as the mask."""
        return img[0:self.height, 0:self.width]