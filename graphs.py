#!/usr/bin/env python

import numpy as np

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


def overall_hist(values, row_id, label):
    values = filter_rows(values, [row_id]).flatten()
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.hist(values, bins=30)
    ax.set_ylabel("Number of datapoints")
    ax.set_xlabel(label)

    fig.legend(loc="upper left")
    fig.show()


def linear_plot(values, x_row_id, y_row_id, x_label, y_label):
    (x, y) = filter_rows(values, [x_row_id, y_row_id])
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.scatter(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    fig.legend(loc="upper left")
    fig.show()


def filter_rows(values, axes):
    out = values[axes, ...]
    # Remove all columns with at least one NaN value
    mask = ~np.isnan(out).any(axis=0)
    return out[:, mask]


def to_frequencies(array, bins=10):
    array = array.flat
    min = np.min(array)
    max = np.max(array)

    arr_range = max - min

    bin_width = arr_range / bins

    out = [[] for i in range(bins)]
    for el in array:
        bin_index = int(np.floor((el - min) / arr_range * bins).item())
        # do not go outside of the array
        if bin_index == bins:
            bin_index = bins - 1
        out[bin_index].append(el)

    out = [[min + (i + 0.5) * bin_width, len(sub_arr)] for i, sub_arr in enumerate(out)]
    return np.array(out).T


# compare_old_and_new()

expected_ndvi_values_label = "Dataset NDVI value"
pop_density_label = "Population density"
pop_density_scaled_label = "ln(population density)"

expected_ndvi_values = [point.get_expected_ndvi() for point in data_points]
population_densities = [point.get_population_density() for point in data_points]
population_densities_scaled = []
for pop in population_densities:
    if pop is None or pop == 0:
        population_densities_scaled.append(None)
    else:
        population_densities_scaled.append(np.log(pop))

data = np.array(
    [expected_ndvi_values, population_densities, population_densities_scaled],
    dtype=float,
)

print("Data generated")

overall_hist(data, 0, expected_ndvi_values_label)
overall_hist(data, 2, pop_density_scaled_label)

frequency_data = to_frequencies(np.array(expected_ndvi_values), bins=30)
print(frequency_data)

linear_plot(
    frequency_data,
    0,
    1,
    "a",
    "b",
)

# do not close the plots immediately
input()
