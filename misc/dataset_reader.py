# Read dataset from specific coordinate
from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def get(self, lat_deg: float, lon_deg: float):
        """Get the dataset value at the coordinates (lat_deg, lon_deg) if possible, else return None"""
        pass


# Read ASC datasets
# More information here: https://support.geocue.com/ascii-raster-files-asc/
class ASCReader(Reader):
    def __init__(self, file: str):
        """Read from an .ASC file"""
        with open(file, "r") as reader:
            """Load properties"""
            self.properties = {}
            line = reader.readline()
            while line[0] not in "-0123456789":
                # Add property
                prop = line.strip().split(" ")  # Remove newline, format
                self.properties[prop[0]] = float(prop[-1])
                line = reader.readline()

            print("ASC", file, self.properties)

            """Load data"""
            self.data = []  # 2D array
            while line != "":
                row = list(map(float, line.strip().split(" ")))  # Convert to floats
                self.data.append(row)
                line = reader.readline()

    # Note that there is a corner case where extreme negative latitudes or positive longitudes result in out-of-bounds error.
    # That will not be fixed as it occurs only for exact points on the boundary that are extremely unlikely to occur during ordinary usage
    def get(self, lat_deg: float, lon_deg: float):
        x_coords = int(
            (lon_deg - self.properties["xllcorner"]) // self.properties["cellsize"]
        )
        y_coords = int(
            (-lat_deg - self.properties["yllcorner"]) // self.properties["cellsize"]
        )  # Reverse y axis as latitude points down

        data = self.data[y_coords][x_coords]

        if data == self.properties["NODATA_value"]: # Return None for useless data
            return None  # No data
        return data
