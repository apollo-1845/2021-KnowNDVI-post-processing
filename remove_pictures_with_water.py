#!/usr/bin/env python

from misc.serialise_data_points import deserialise_from_prompt, serialise_from_prompt
import numpy as np

data_points = deserialise_from_prompt()

data_points = np.array([point for point in data_points if point.get_landtype() != 0])

print(data_points.size)
print(data_points)

serialise_from_prompt(data_points, "no_sea")
