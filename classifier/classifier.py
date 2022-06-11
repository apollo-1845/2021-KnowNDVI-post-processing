# Using a TensorFlow Neural Network to predict where land is
import cv2
import numpy as np

from settings import CLASSIFIER_CERTAINTY_THRESHOLD as CERTAINTY_THRESHOLD
from settings import CLASSIFIER_TILE_SIZE as TILE_SIZE

"""Constants for cropping image to place in model"""
from settings import CLASSIFIER_CROP_SIZE as CROP_SIZE

PIXELS_TO_CENTRE = CROP_SIZE // 2
PIXELS_TO_CENTRE_2 = CROP_SIZE - PIXELS_TO_CENTRE


class Classifier:
    """Using a TensorFlow Neural Network to predict where land is. Create a `Classifier`, then `predict_image` to get the land mask."""

    def __init__(self, channels, model):
        """Create a `Classifier`"""
        # Save channels
        self.nir, self.vis, self.ndvi = channels

        # Save NN
        self.model = model

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

        if (start_y < 0):
            for i in range(CROP_SIZE - nir_crop.shape[0]):
                empty_line = Classifier.create_empty_col(nir_crop.shape[1])  # Width
                nir_crop = np.vstack([empty_line, nir_crop])  # Vertical, before
                vis_crop = np.vstack([empty_line, vis_crop])  # Vertical, before
                ndvi_crop = np.vstack([empty_line, ndvi_crop])  # Vertical, before
            # print("-y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        elif (end_y > height):
            for i in range(CROP_SIZE - nir_crop.shape[0]):
                empty_line = Classifier.create_empty_col(nir_crop.shape[1])  # Width
                nir_crop = np.vstack([nir_crop, empty_line])  # Vertical, after
                vis_crop = np.vstack([vis_crop, empty_line])  # Vertical, after
                ndvi_crop = np.vstack([ndvi_crop, empty_line])  # Vertical, after
            # print("+y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        if (start_x < 0):
            for i in range(CROP_SIZE - nir_crop.shape[1]):
                empty_line = Classifier.create_empty_row(nir_crop.shape[0])  # Height
                nir_crop = np.hstack([empty_line, nir_crop])  # Horizontal, before
                vis_crop = np.hstack([empty_line, vis_crop])  # Horizontal, before
                ndvi_crop = np.hstack([empty_line, ndvi_crop])  # Horizontal, before
                # print(nir_crop)
            # print("-x>", nir_crop.shape, vis_crop.shape, start_x, start_y)
        elif (end_x > width):
            for i in range(CROP_SIZE - nir_crop.shape[1]):
                empty_line = Classifier.create_empty_row(nir_crop.shape[0])  # Height
                nir_crop = np.hstack([nir_crop, empty_line])  # Horizontal, after
                vis_crop = np.hstack([vis_crop, empty_line])  # Horizontal, after
                ndvi_crop = np.hstack([ndvi_crop, empty_line])  # Horizontal, after
            # print("+x>", nir_crop.shape, vis_crop.shape, start_x, start_y)

        return nir_crop, vis_crop, ndvi_crop

    def predict_image(self):
        """Return a mask of which pixels are land from the nir, vis and ndvi channels. If this is slow, update `settings."""
        crops = []

        height = (self.vis.shape[1] // TILE_SIZE) * TILE_SIZE  # Multiple of tile_size
        width = (self.vis.shape[1] // TILE_SIZE) * TILE_SIZE  # Multiple of tile_size

        for y in range(0, height, TILE_SIZE):
            for x in range(0, width, TILE_SIZE):
                crop = np.array(self.get_crop(x, y))
                # cv2_imshow(crop[1])
                # print(x, y, nir[y, x], vis[y, x])
                # cv2_imshow(crop[1])
                crops.append(crop)

        crops = np.array(crops)
        prediction = self.model.predict(crops)
        prediction = np.reshape(prediction, (height // TILE_SIZE, width // TILE_SIZE))  # grid
        prediction = cv2.resize(prediction, None, None, TILE_SIZE, TILE_SIZE, cv2.INTER_NEAREST)  # Nearest neighbour

        return self.prediction_to_mask(prediction)

    def prediction_to_mask(self, prediction):
        mask = prediction

        # Double-check to remove large clouds with thresholds
        total = (self.nir.astype("float") + self.vis.astype("float"))
        mask[total > 310] = 0  # 310 # Remove clouds by colour
        mask[total < 200] = 0  # 310 # Remove sea by colour

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (32, 32))
        mask = cv2.filter2D(mask, -1, kernel) / kernel.sum()  # Convolution to favour large land masses

        # Remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6)))

        # DEBUG - show mask on image
        result = self.vis.copy()
        result[mask < CERTAINTY_THRESHOLD] = result[mask < 0.15] // 3
        # Display
        title = "Classifier mask preview"
        cv2.namedWindow(title)  # create window
        cv2.imshow(title, result)  # display image
        cv2.waitKey(0)  # wait for key press
        cv2.destroyAllWindows()

        return mask < CERTAINTY_THRESHOLD

    @staticmethod
    def create_empty_col(length):
        """Padding for crops - Create a line of zeros all in a 1-item array of len length"""
        return np.zeros(length)

    @staticmethod
    def create_empty_row(length):
        """Padding for crops - Create a line of zeros each in a 1-item array of len length"""
        return np.array([np.array([0]) for x in range(length)])
