#!/usr/bin/env python

import numpy as np
from math import log

import matplotlib as mpl
import matplotlib.pyplot as plt

from remove_overlapping_pictures import get_spherical_distance

from misc.serialise_data_points import deserialise_from_prompt, deserialise_from_file

data_points = deserialise_from_prompt()


# timestamps = [point.get_timestamp().get_raw() for point in data_points]
latitudes = [point.get_coordinates()[0] for point in data_points]
longitudes = [point.get_coordinates()[1] for point in data_points]


def compare_old_and_new():
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    data_points_full = deserialise_from_file(f"./intermediates/full_data.json")
    data_points_full = [point for point in data_points_full]

    # timestamps_full = [point.get_timestamp().get_raw() for point in data_points_full]
    latitudes_full = [point.get_coordinates()[0] for point in data_points_full]
    longitudes_full = [point.get_coordinates()[1] for point in data_points_full]

    ax.scatter(longitudes_full, latitudes_full, c="blue", label="Full data from ISS")
    ax.scatter(longitudes, latitudes, c="orange", label="New data")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Coordinates of taken pictures")

    fig.legend(loc="upper left")
    fig.show()


def overall_hist(values, label):
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.hist(values, bins=30)
    ax.set_ylabel("Number of datapoints")
    ax.set_xlabel(label)

    fig.legend(loc="upper left")
    fig.show()


def linear_plot(x, y, x_label, y_label):
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.scatter(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    fig.legend(loc="upper left")
    fig.show()


def remove_none(arr):
    return list(filter(None, arr))


# compare_old_and_new()

expected_ndvi_values = [point.get_expected_ndvi() for point in data_points]
expected_ndvi_values = remove_none(expected_ndvi_values)
expected_ndvi_values_label = "Dataset NDVI value"

population_densities = [point.get_population_density() for point in data_points]
population_densities_scaled = [
    log(point) for point in population_densities if point is not None
]
population_densities = remove_none(population_densities)

pop_density_scaled_label = "ln(population density)"

overall_hist(expected_ndvi_values, expected_ndvi_values_label)
overall_hist(population_densities_scaled, pop_density_scaled_label)

# linear_plot(
#     population_densities_scaled,
#     expected_ndvi_values,
#     pop_density_scaled_label,
#     expected_ndvi_values_label,
# )
# wait for the plot to be closed
input()
