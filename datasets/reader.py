# Read dataset from specific coordinate
from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def get(self, lat_deg: float, lon_deg: float):
        """Get the dataset value at the coordinates (lat_deg, lon_deg) if possible, else return None"""
        pass


# Read ASC datasets
class ASCReader:
    def __init__(self, file: str):
        """Read from an .ASC file"""
        with open(file, "r") as reader:
            """Load properties"""
            self.properties = {}
            line = reader.readline()
            while (line[0] not in "0123456789"):
                # Add property
                prop = line.strip().split(" ")  # Remove newline, format
                self.properties[prop[0]] = float(prop[1])
                line = reader.readline()

            """Load data"""
            self.data = []  # 2D array
            while (line != ""):
                row = list(
                    map(
                        float,  # Convert to floats
                        line.split(" ")
                    )
                )
                self.data.append(row)
                line = reader.readline()

        """Can the width/height be wrapped?"""
        self.continuous_width = self.properties["ncols"] == 360
        self.continuous_height = self.properties["nrows"] == 180

    def get(self, lat_deg: float, lon_deg: float):
        x_coords = int((lon_deg - self.properties["xllcorner"]) // self.properties["cellsize"])
        y_coords = int((-lat_deg - self.properties["yllcorner"]) // self.properties[
            "cellsize"])  # Reverse y axis as latitude points down
        # if(x_coords < 0) or (y_coords < 0) or (x_coords > self.properties["ncols"]) or (y_coords > self.properties["nrows"]):
        #     return None # Out of range
        if (self.continuous_width):
            x_coords %= 360
        if (self.continuous_height):
            y_coords %= 180

        # print(lon_deg, x_coords, lat_deg, y_coords)

        # print(x_coords, y_coords)
        data = self.data[y_coords][x_coords]
        if (data == self.properties["NODATA_value"]):
            return None  # No data
        return data

# landclass = ASCReader("./data/modis_landcover_class_qd.asc")
# print(landclass.get(-52, -73))
