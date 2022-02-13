# Read results from ISS saved data
import numpy as np


class ResultReader:
    def __init__(self, file, sensors):
        print("Open")
        self.sensors = sensors
        self.reader = open(file, "rb")

    def read_raw(self):
        sensor_num_byte = self.reader.read(1)
        while(len(sensor_num_byte) > 0):
            # Sensor number
            sensor_num = int(np.frombuffer(sensor_num_byte, "uint8")) # Read 1 byte
            # Length of reading in bytes
            reading_len = int(np.frombuffer(self.reader.read(1), "uint8"))  # Read 1 byte
            # Reading data
            data = self.reader.read(reading_len)  # Read len bytes
            yield sensor_num, data

            # Get byte for sensor number so can check for EOF
            sensor_num_byte = self.reader.read(1)

    def read(self):
        for sensor_num, data in self.read_raw():
            sensor = self.sensors[sensor_num]
            yield sensor, data

    def close(self):
        print("Close")
        self.reader.close()

sensors = [TimeStampData]
reader = ResultReader("results/out.blob", ["timestamp", "camera"])
for sensor, data in reader.read():
    print(sensor, data)
reader.close()