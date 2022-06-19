# Debug functions
import os

from parseBlob import parse_blob


def get_datapoints(start_id: int, end_id: int = None, step:int = 1):
    """A generator of (id_num, datapoint) for debug purposes"""
    if(end_id is None): end_id = start_id
    # Get dp
    data_points = parse_blob(os.path.join("data", "other", "out.blob"))
    i = 1
    for point in data_points:
        if(i % step != 0):
            # print(i, "not stepped on")
            pass
        elif (i > end_id):
            # print(i, "at end")
            break
        elif (i >= start_id):
            yield i, point
        else:
            # print(i, "before start")
            pass
        i += 1