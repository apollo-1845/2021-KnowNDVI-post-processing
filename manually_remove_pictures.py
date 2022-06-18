#!/usr/bin/env python

from misc.serialise_data_points import deserialise_from_prompt, serialise_from_prompt
import numpy as np
import cv2
from time import sleep

data_points = deserialise_from_prompt()

filtered_data_points = []
skip_num = 0
for point in data_points:
    id = point.get_id()
    # skip the point
    if skip_num > id:
        continue

    print("Picture id:", id, "coords:", point.get_coordinates())

    image = point.get_camera_data()  # Falkland Islands
    image.open()
    while True:
        # Keep on displaying the image and checking if the key is pressed
        choice = cv2.waitKey(1)
        if choice == ord("y"):  # yes
            image.close()
            filtered_data_points.append(point)
            break
        elif choice == ord("n"):  # no
            image.close()
            break
        elif choice == ord("s"):  # skip
            image.close()
            skip_num = int(input("What item to skip to (or past)?"))
            break
    sleep(0.200)

print(len(filtered_data_points))

serialise_from_prompt(filtered_data_points, "manually_filtered")
