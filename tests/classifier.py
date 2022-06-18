#!/usr/bin/env python
import os
import time

from classifier.predict import Classifier
from parseBlob import parse_blob
from results.data_point import DataPoint

import tensorflow as tf
import numpy as np
print("TF Version", tf.__version__)

from tensorflow import keras # Trained and created separately; load the TF model into the classifier
import cv2

def get_datapoints(start_id: int, end_id: int) -> DataPoint:
    # Get dp
    data_points = parse_blob(os.path.join("data", "other", "out.blob"))
    i = 1
    for point in data_points:
        if (i > end_id):
            break
        elif (i >= start_id):
            yield point
        i += 1

# def get_dp_by_longitude(long:int) -> DataPoint:
#     # Get dp
#     data_points = parse_blob(os.path.join("data", "other", "out.blob"))
#     for point in data_points:
#         if (point.get_coordinates()[1]-long) < 0.001:
#             return point


def run_test():
    # Load NN model
    print("Loading model...")
    model = keras.models.load_model(os.path.join("data", "classifier", "model"))

    model.summary()

    # Get mask
    for i, datapoint in enumerate(get_datapoints(660, 680)):  # Falkland Islands
        print("Image", i)
        start = time.time()
        ndvi = datapoint.get_land_masked(model, datapoint.get_ndvi())
        end = time.time()
        print("Mean NDVI", np.mean(ndvi))
        print("Took", end-start, "s to generate land-masked list of NDVIs")