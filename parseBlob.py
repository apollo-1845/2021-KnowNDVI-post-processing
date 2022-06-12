#!/usr/bin/env python
from results.data_point import DataPoint
from settings import OUT_FILE
import numpy as np
from misc.dataset_reader import ASCReader

from misc.serialise_data_points import serialise_from_prompt


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


data_points = parse_blob(OUT_FILE)

serialise_from_prompt(data_points, "full_data")
