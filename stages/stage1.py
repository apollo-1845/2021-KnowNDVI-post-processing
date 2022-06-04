# Read out from ISS saved data

from project_types import DataPoint
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData
from settings import OUT_FILE
import time

import numpy as np

from datasets.reader import ASCReader


# class ResultReader:
#     def __init__(self, file):
#         print("Open")
#         self.reader = open(file, "rb")

#     def read_data(self):
#         sensor_num_byte = self.reader.read(1)
#         while (len(sensor_num_byte) > 0):
#             # Sensor number
#             sensor_num = int(np.frombuffer(sensor_num_byte, "uint8"))  # Read 1 byte
#             # Length of reading in bytes
#             reading_len = int(np.frombuffer(self.reader.read(4), "uint32"))  # Read 4 bytes
#             # Reading data
#             data = self.reader.read(reading_len)  # Read len bytes
#             yield sensor_num, data

#             # Get byte for sensor number so can check for EOF
#             sensor_num_byte = self.reader.read(1)

#     def read_groups(self):
#         """A generator to yield each group of data from the sensors in the order of the sensors"""
#         current_group = tuple()
#         for sensor_num, data in self.read_data():
#             if(sensor_num == 0 and len(current_group) > 0):
#                 # First sensor - new group
#                 yield current_group
#                 current_group = ()
#             # Add to group
#             current_group += (data,)

#         # Last group
#         yield current_group

#     def close(self):
#         print("Close")
#         self.reader.close()


def parse_blob(fileName):
    file = open(fileName, "rb")

    # a read with a check for EOF
    def read_check_EOF(num):
        out = file.read(num)
        # unexpected EOF
        if len(out) != num:
            raise EOFError("Unexpected EOF - looks like there are no data_points left.")
        return out

    data_types = [TimeStampData, CameraData]

    # a partially parsed value indicates that something went wrong when parsing
    data_point_completely_parsed = True

    # Find first sensor ID
    sensor_id_byte = read_check_EOF(1)

    while True:
        # Get byte for sensor number so can check for EOF
        try:
            data_point_params = []
            for data_type_id in range(len(data_types)):
                data_type = data_types[data_type_id]
                # Sensor number
                parsed_sensor_id = int(
                    np.frombuffer(sensor_id_byte, "uint8")
                )  # Read 1 byte
                assert parsed_sensor_id == data_type_id

                # we have started parsing the value - we would hope there is no EOF in the middle of a datapoint
                data_point_completely_parsed = False

                # Length of reading in bytes
                encoded_data_len = int(
                    np.frombuffer(read_check_EOF(4), "uint32")
                )  # Read 4 bytes

                # Reading data
                encoded_data = read_check_EOF(encoded_data_len)  # Read len bytes
                data_point_params.append(data_type.deserialise(encoded_data))

                data_point_completely_parsed = True

                # Get byte for sensor number so can check for EOF
                sensor_id_byte = read_check_EOF(1)

            yield DataPoint(*data_point_params)
        except EOFError as e:
            # if normal end of file, simply return
            if data_point_completely_parsed:
                return
            else:
                raise e


def run():
    """Input files and parse into data points"""
    data_points = parse_blob(OUT_FILE)

    return data_points


# landtype = ASCReader(
#     "data/modis_landcover_class_qd.asc"
# )  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png

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
