#!/usr/bin/env python

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from misc.serialise_data_points import deserialise_from_file

# An example name could be 'full_data'
# fileName = input('Input file name:')
fileName = "full_data"
data_points = deserialise_from_file(f"./intermediates/{fileName}.json")

data_points = np.array([point for point in data_points])
print("Number of items: ", len(data_points))

fig, ax = plt.subplots()  # Create a figure containing a single axes.

timestamps = [point.get_timestamp().get_raw() for point in data_points]
latitudes = [point.get_coordinates()[0] for point in data_points]
longitudes = [point.get_coordinates()[1] for point in data_points]

ax.plot(timestamps, latitudes)
# ax.plot(longitudes, latitudes)
# ax.plot([i for i in range(len(data_points))], timestamps)
# ax.plot([i for i in range(len(data_points))], latitudes)
# Plot some data on the axes.

fig.show()

# wait for the plot to be closed
input()
