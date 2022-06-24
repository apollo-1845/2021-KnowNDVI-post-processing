from copy import deepcopy

import numpy as np

from misc.serialise_data_points import deserialise_from_prompt, serialise_from_prompt

if __name__ == "__main__":
    data_points = deserialise_from_prompt("manually_filtered")
    new_data_points = []
    for point in data_points:
    #     # Get NDVI - lazy evaluation
    #     print("Land type:", point.get_land_cover())
    #     # Mask is not working very well - targets the edges of clouds + parts of sea
    #     print("NDVI:", point.get_avg_ndvi(), "Expected", point.get_expected_ndvi())
    #     new_data_points.append(point)
        # Get datapoints, one for each NDVI
        print(point.get_id())
        ndvis = point.get_land_masked(point.get_ndvi())
        print(ndvis.shape)
        for y in range(0, ndvis.shape[0], 50): # Height
            for x in range(0, ndvis.shape[0], 50):  # Width
                # print("i", i)
                pxpoint = deepcopy(point)
                pxpoint._avg_ndvi = np.mean(ndvis[y:y+50, x:x+50])
                # print(pxpoint._avg_ndvi)
                new_data_points.append(pxpoint)

    serialise_from_prompt(new_data_points, "ndvi_processed")