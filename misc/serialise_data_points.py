#!/usr/bin/env python

from results.data_point import DataPoint
import numpy as np
import json


def serialise_data_points(data_points):
    out = []
    for point in data_points:
        out.append(point.serialise())
    return json.dumps(out)


# Note that it should override the file data
def serialise_to_file(file_name, data_points):
    with open(file_name, "w") as f:
        f.write(serialise_data_points(data_points))


def deserialise_from_file(file_name):
    fileData = None
    with open(file_name, "r") as f:
        fileData = f.read()
    return deserialise_data_points(fileData)


def deserialise_data_points(string):
    serialised_data_points = json.loads(string)
    for point in serialised_data_points:
        yield DataPoint.deserialise(point)


def deserialise_from_prompt(default_name="full_data"):
    # An example name could be 'full_data'
    file_name = input(f"Input file name (blank for '{default_name}'):")
    if file_name == "":
        file_name = default_name
    data_points = deserialise_from_file(f"./intermediates/{file_name}.json")

    data_points = np.array([point for point in data_points])
    print("Number of items: ", len(data_points))
    return data_points


def serialise_from_prompt(data_points, default_name=None):
    file_name = None
    if default_name is not None:
        file_name = input(f"Output file name(blank for '{default_name}'):")
        if file_name == "":
            file_name = default_name
    else:
        file_name = input("Output file name:")
    serialise_to_file(f"./intermediates/{file_name}.json", data_points)
