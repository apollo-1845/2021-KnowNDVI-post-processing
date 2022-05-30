# Read out from ISS saved data
import time

import numpy as np

from results.timestamp_data import TimeStampData
from results.camera_data import CameraData
from datasets.reader import ASCReader


class ResultReader:
    def __init__(self, file):
        print("Open")
        self.reader = open(file, "rb")

    def read_data(self):
        sensor_num_byte = self.reader.read(1)
        while (len(sensor_num_byte) > 0):
            # Sensor number
            sensor_num = int(np.frombuffer(sensor_num_byte, "uint8"))  # Read 1 byte
            # Length of reading in bytes
            reading_len = int(np.frombuffer(self.reader.read(4), "uint32"))  # Read 4 bytes
            # Reading data
            data = self.reader.read(reading_len)  # Read len bytes
            yield sensor_num, data

            # Get byte for sensor number so can check for EOF
            sensor_num_byte = self.reader.read(1)

    def read_groups(self):
        """A generator to yield each group of data from the sensors in the order of the sensors"""
        current_group = tuple()
        for sensor_num, data in self.read_data():
            if(sensor_num == 0 and len(current_group) > 0):
                # First sensor - new group
                yield current_group
                current_group = ()
            # Add to group
            current_group += (data,)

        # Last group
        yield current_group

    def close(self):
        print("Close")
        self.reader.close()


reader = ResultReader("out/out.blob")
landtype = ASCReader(
    "data/modis_landcover_class_qd.asc")  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png

start = time.time()
i = 0
type_freqs = [0 for i in range(20)]

best_image = None
least_unusable = float("inf")

total_mean = np.zeros(20)
total_weight = np.zeros(20)

for timestamp, photo in reader.read_groups():
    # if(i % 100 == 0):
    timestamp = TimeStampData.deserialise(timestamp)
    loc = timestamp.to_location()
    type = int(landtype.get(loc[0], loc[1]))

    type_freqs[type] += 1

    if (type != 0):
        print(i, "🌍", loc, type)
        photo = CameraData.deserialise(photo)
        # photo.display()
        ndvi = photo.get_ndvi()
        unusable = ndvi.get_unusable_area()

        mean, weight = ndvi.get_mean_and_weight()
        total_mean[type] += mean
        total_weight[type] += weight

        if (unusable < least_unusable):
            least_unusable = unusable
            best_image = i

        ndvi.contrast()
        ndvi.display()
    i += 1
    # if(i > 1000): break

print("Mean NDVI values: ",
      total_mean / total_weight)  # TODO: Add inner-image filtering etc. to make this make sense. (It's currently saying that snow and ice has a lot of plant cover)

print(best_image)

end = time.time()

print("Took ", end - start)
print(type_freqs)

reader.close()
