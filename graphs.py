#!/usr/bin/env python

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from classifier.predict import load_model

from remove_overlapping_pictures import get_spherical_distance

from misc.serialise_data_points import deserialise_from_prompt, deserialise_from_file

load_model()

data_points = deserialise_from_prompt()

fig, ax = plt.subplots()  # Create a figure containing a single axes.

timestamps = [point.get_timestamp().get_raw() for point in data_points]
latitudes = [point.get_coordinates()[0] for point in data_points]
longitudes = [point.get_coordinates()[1] for point in data_points]


def compare_filtered_and_unfiltered():
    data_points_full = deserialise_from_file(f"./intermediates/full_data.json")
    data_points_full = [point for point in data_points_full]

    timestamps_full = [point.get_timestamp().get_raw() for point in data_points_full]
    latitudes_full = [point.get_coordinates()[0] for point in data_points_full]
    longitudes_full = [point.get_coordinates()[1] for point in data_points_full]

    ax.scatter(longitudes_full, latitudes_full, c="blue", label="Full")
    ax.scatter(longitudes, latitudes, c="orange", label="Filtered")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Coordinates of taken pictures")


prev_point = None
for point in data_points:
    if prev_point is None:
        print(point.get_id())
    else:
        (lat1, long1) = point.get_coordinates()
        (lat2, long2) = prev_point.get_coordinates()
        print(
            point.get_ndvi(),
            point.get_masked_ndvi_values(),
            point.get_id(),
            (lat1, long1),
            (lat2, long2),
            get_spherical_distance(lat1, long1, lat2, long2),
        )
    prev_point = point

compare_filtered_and_unfiltered()

fig.legend(loc="upper left")

fig.show()

# wait for the plot to be closed
input()
