#!/usr/bin/env python

from misc.serialise_data_points import deserialise_from_prompt, serialise_from_prompt
from math import radians, pow, sin, cos, asin, sqrt

data_points = deserialise_from_prompt()

# NOTE This is a very crude way of doing this

# Calculated using a picture of Falkland Islands
KM_VIEW_DIAMETER = 404

KM_EARTH_RADIUS = 6371

new_data_points = []
last_radian_coords = None


def get_radian_coords(point):
    coords = point.get_coordinates()
    return (radians(coords[0]), radians(coords[1]))


for point in data_points:
    current_radian_coords = get_radian_coords(point)
    if len(new_data_points) == 0:
        new_data_points.append(point)
        last_radian_coords = current_radian_coords
    else:
        (lat1, long1) = last_radian_coords
        (lat2, long2) = current_radian_coords
        # Using the Haversine formula
        term1 = pow(sin((lat2 - lat1) / 2), 2)
        term2 = pow(sin((long2 - long1) / 2), 2)

        km_dist = term1 + cos(lat1) * cos(lat2) * term2

        km_dist = 2 * KM_EARTH_RADIUS * asin(sqrt(km_dist))

        if km_dist > KM_VIEW_DIAMETER:
            last_radian_coords = current_radian_coords
            new_data_points.append(point)


serialise_from_prompt(new_data_points, "no_overlapping")
