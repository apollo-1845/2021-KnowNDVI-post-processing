# Read out from ISS saved data
from results.data_point import DataPoint
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData
from settings import OUT_FILE
import time

import numpy as np

from datasets.reader import ASCReader


def parse_blob(fileName):
    file = open(fileName, "rb")

    # a read with a check for EOF
    def read_check_EOF(num):
        out = file.read(num)
        # unexpected EOF
        if len(out) != num:
            raise EOFError("Unexpected EOF - looks like there are no data_points left.")
        return out

    data_types_num = 2
    # a partially parsed value indicates that something went wrong when parsing
    data_point_completely_parsed = True

    while True:
        try:
            data_point_params = []
            for data_type_id in range(data_types_num):
                # Get byte for sensor number so can check for EOF
                sensor_id_byte = read_check_EOF(1)

                # we have started parsing the value - we would hope there is no EOF in the middle of a datapoint
                data_point_completely_parsed = False

                # Sensor number
                parsed_sensor_id = int(
                    np.frombuffer(sensor_id_byte, "uint8")
                )  # Read 1 byte
                assert parsed_sensor_id == data_type_id

                # Length of reading in bytes
                encoded_data_len = int(
                    np.frombuffer(read_check_EOF(4), "uint32")
                )  # Read 4 bytes

                # Reading data
                encoded_data = read_check_EOF(encoded_data_len)  # Read len bytes
                data_point_params.append(encoded_data)

            data_point_completely_parsed = True

            yield DataPoint(*data_point_params)
        except EOFError as e:
            # if normal end of file, simply return
            if data_point_completely_parsed:
                return
            else:
                raise e


def run():
    """Input files and parse into data points"""
    return parse_blob(OUT_FILE)

    # for point in data_points_generator:
    #     print(point.get_coordinates())


# start = time.time()
# i = 0
# type_freqs = [0 for i in range(20)]

# best_image = None
# least_unusable = float("inf")

# total_mean = np.zeros(20)
# total_weight = np.zeros(20)

# for timestamp, photo in reader.read_groups():
#     # if(i % 100 == 0):
#     timestamp = TimeStampData.deserialise(timestamp)
#     loc = timestamp.to_location()
#     type = int(landtype.get(loc[0], loc[1]))

#     type_freqs[type] += 1

#     if type != 0:
#         print(i, "🌍", loc, type)
#         photo = CameraData.deserialise(photo)
#         # photo.display()
#         ndvi = photo.get_ndvi()
#         unusable = ndvi.get_unusable_area()

#         mean, weight = ndvi.get_mean_and_weight()
#         total_mean[type] += mean
#         total_weight[type] += weight

#         if unusable < least_unusable:
#             least_unusable = unusable
#             best_image = i

#         ndvi.contrast()
#         ndvi.display()
#     i += 1
#     # if(i > 1000): break

# print(
#     "Mean NDVI values: ", total_mean / total_weight
# )  # TODO: Add inner-image filtering etc. to make this make sense. (It's currently saying that snow and ice has a lot of plant cover)

# print(best_image)

# end = time.time()

# print("Took ", end - start)
# print(type_freqs)

# reader.close()
