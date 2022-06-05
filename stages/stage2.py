# Apply filtering for clouds + sea
import copy

import cv2
import numpy as np

from results.camera_data import CameraData


# def run(data_points):
#     """Filter images from data point iterator, creating discarding masks with np.nan"""
#     for point in data_points:
#         point.image = filter(point.image) # Filter each separately
#         yield point

def filter(image: CameraData):
    """Filter clouds and sea"""
    # Clouds
    # # DEBUG - BFS
    # threshold_diffs = [1, 256]
    # thresholds = [1, 256]
    # while(threshold_diffs[0] >= 0.02 and threshold_diffs[1] >= 2):
    #     img = copy.deepcopy(image)
    #     img.display()
    #     img.mask_sea(*thresholds)
    #     img.display()
    #
    #     for i in range(len(thresholds)):
    #         print("Higher is less blue" if i == 0 else "Higher is lighter")
    #         answer = input("[h]igher, [l]ower, or [q]uit if good. ").lower()
    #         threshold_diffs[i] /= 2
    #         if(answer == "h"):
    #             thresholds[i] += threshold_diffs[i]
    #         elif(answer == "l"):
    #             thresholds[i] -= threshold_diffs[i]
    #         elif(answer == "q"):
    #             break
    #     else:
    #         continue
    #     break # Broke from inside
    #
    # print("Thresholds:", thresholds)

    image.mask_lighter_total(310)  # Cloud threshold - TODO: Improve - more precise
    image.mask_sea(225)  # Sea threshold - TODO: Improve - change algorithm / channel specific?

    print(np.nanpercentile(image.image, 25, axis=0), np.nanpercentile(image.image, 75))

    # print(np.nan in image.image)
    # image.image[image.image == np.nan] = 0
    # print(np.nan in image.image)
    # image.image = cv2.morphologyEx(image.image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, [20, 20]))
    # image.image[image.image == 0] = np.nan

    # image.image = cv2.morphologyEx(image.image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, [5, 5]))
    return image


# DEBUG
for i in [670]:  # [1, 200, 670, 1880]:
    image = CameraData.deserialise((i).to_bytes(4, "big"))  # Falkland Islands
    image.display()
    image = filter(image)
    image.display()
    image = image.get_ndvi()
    image.contrast()
    image.display()
