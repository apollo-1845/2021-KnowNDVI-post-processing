#!/usr/bin/env python
import time

from debug_funcs import get_datapoints
from classifier.predict import load_model

import tensorflow as tf
import numpy as np

print("TF Version", tf.__version__)

# def get_dp_by_longitude(long:int) -> DataPoint:
#     # Get dp
#     data_points = parse_blob(os.path.join("data", "other", "out.blob"))
#     for point in data_points:
#         if (point.get_coordinates()[1]-long) < 0.001:
#             return point


def run_test():
    # Load NN model
    load_model()

    # Get mask
    for i, datapoint in enumerate(get_datapoints(660, 680)):  # Falkland Islands
        print("Image", i)
        start = time.time()
        ndvi = datapoint.get_land_masked(datapoint.get_ndvi())
        end = time.time()
        print("Mean NDVI", np.mean(ndvi))
        print("Took", end - start, "s to generate land-masked list of NDVIs")
