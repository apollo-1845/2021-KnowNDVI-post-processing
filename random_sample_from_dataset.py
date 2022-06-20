#!/usr/bin/env python

from results.data_point import DataPoint
from misc.serialise_data_points import serialise_from_prompt
from random import random

if __name__ == "__main__":
    sample_size = int(input("Sample size: "))

    sample = []

    # returns a uniformly random number in range [min, max)
    def random_float_range(min, max):
        return (max - min) * random() + min

    while len(sample) < sample_size:
        coords = (random_float_range(-90, 90), random_float_range(-180, 180))

        potential_data_point = DataPoint.from_coordinates(coords)

        # check if applicable
        if potential_data_point.get_expected_ndvi() is not None:
            sample.append(potential_data_point)

    serialise_from_prompt(sample, "expected_sample")
