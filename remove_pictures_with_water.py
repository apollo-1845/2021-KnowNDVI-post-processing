#!/usr/bin/env python

from misc.serialise_data_points import deserialise_from_prompt, serialise_from_prompt
import numpy as np

data_points = deserialise_from_prompt()

data_points = np.array([point for point in data_points if point.get_land_cover() != 0])

print("Data points:", data_points.size)

serialise_from_prompt(data_points, "no_sea")
