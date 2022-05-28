# Read out from ISS saved data
import time

import numpy as np

from results.timestamp_data import TimeStampData
from results.camera_data import CameraData


class ResultReader:
    def __init__(self, file, in_types):
        print("Open")
        self.in_types = in_types
        self.reader = open(file, "rb")

    def read_raw(self):
        sensor_num_byte = self.reader.read(1)
        while(len(sensor_num_byte) > 0):
            # Sensor number
            sensor_num = int(np.frombuffer(sensor_num_byte, "uint8")) # Read 1 byte
            # Length of reading in bytes
            reading_len = int(np.frombuffer(self.reader.read(4), "uint32"))  # Read 4 bytes
            # Reading data
            data = self.reader.read(reading_len)  # Read len bytes
            yield sensor_num, data

            # Get byte for sensor number so can check for EOF
            sensor_num_byte = self.reader.read(1)

    def read_data(self):
        for sensor_num, data in self.read_raw():
            in_type = self.in_types[sensor_num]
            yield sensor_num, in_type.deserialise(data)

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


in_types = [TimeStampData, CameraData]
reader = ResultReader("out/out.blob", in_types)

start = time.time()
i = 0
for timestamp, photo in reader.read_groups():
    if(i % 600 == 0):
        print("@", timestamp)
        photo.display()
        ndvi = photo.get_ndvi()
        ndvi.display()
    i += 1

end = time.time()

print("Took ", end-start)

reader.close()