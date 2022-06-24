#!/usr/bin/env python
import time

from debug_funcs import get_datapoints

# import tensorflow as tf
import numpy as np

# print("TF Version", tf.__version__)

# def get_dp_by_longitude(long:int) -> DataPoint:
#     # Get dp
#     data_points = parse_blob(os.path.join("data", "other", "out.blob"))
#     for point in data_points:
#         if (point.get_coordinates()[1]-long) < 0.001:
#             return point


def run_test():
    # Get mask
    for i, datapoint in get_datapoints(600, 4000, 10): #list(get_datapoints(1800, 1900, 10)) +
        if datapoint.get_land_cover() != 0 and np.mean(datapoint.get_camera_data().image) > 10:  # Only on light land
            print("Image", i)
            print(datapoint.get_coordinates())
            start = time.time()
            ndvi = datapoint.get_land_masked(datapoint.get_ndvi())
            end = time.time()
            print("Mean NDVI", np.nanmean(ndvi), "Expected", datapoint.get_expected_ndvi())
            print("Took", end - start, "s to generate land-masked list of NDVIs")
