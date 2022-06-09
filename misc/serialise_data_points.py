#!/usr/bin/env python

from results.data_point import DataPoint
import json


def serialise_data_points(data_points):
    out = []
    for point in data_points:
        out.append(point.serialise())
    return json.dumps(out)


# Note that it should override the file data
def serialise_to_file(fileName, data_points):
    with open(fileName, "w") as f:
        f.write(serialise_data_points(data_points))


def deserialise_from_file(fileName):
    fileData = None
    with open(fileName, "r") as f:
        fileData = f.read()
    return deserialise_data_points(fileData)


def deserialise_data_points(string):
    serialised_data_points = json.loads(string)
    for point in serialised_data_points:
        yield DataPoint.deserialise(point)
