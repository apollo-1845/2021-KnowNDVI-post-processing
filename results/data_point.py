#!/usr/bin/env python
import math
import urllib
from copy import deepcopy

import cv2
import numpy as np
import requests
import urllib3

from misc.dataset_reader import ASCReader
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData

# A helpful site for debugging: https://www.findlatitudeandlongitude.com/
from settings import GGLMAPS_KEY

"""Datasets"""
expected_ndvi = ASCReader("data/datasets/ndvi.asc")
land_cover = ASCReader(
    "data/datasets/land_cover.asc"
)  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png

population_density = ASCReader("data/datasets/population_density.asc")
co2_emissions = ASCReader("data/datasets/co2_emissions.asc")
historical_land_use = ASCReader("data/datasets/historical_land_use.asc")
gdp = ASCReader("data/datasets/gdp.asc")
precipitation = ASCReader("data/datasets/precipitation.asc")
temperature = ASCReader("data/datasets/temperature.asc")
radiation = ASCReader("data/datasets/radiation.asc")


artificial_data_point_id = 0


def remove_none_or_negative(val):
    if val is None or val < 0:
        return None
    return val


class DataPoint:
    """A class representing a collection of available data for a certain timestamp and position"""

    def __init__(self):
        self._coordinates = None
        self._camera_data = None
        self._masked_ndvi = None
        self._timestamp = None
        self._id = None
        self._camera_data_raw = None

        self._avg_ndvi = None

    @staticmethod
    def from_timestamp(timestamp, camera_data_raw, avg_ndvi=None):
        out = DataPoint()
        out._id = int.from_bytes(camera_data_raw, byteorder="big")
        out._camera_data_raw = camera_data_raw
        out._avg_ndvi = avg_ndvi

        out._timestamp = timestamp

        return out

    def from_coordinates(coords):
        global artificial_data_point_id
        out = DataPoint()

        out._id = artificial_data_point_id
        artificial_data_point_id += 1

        out._coordinates = coords

        return out

    def get_id(self):
        return self._id

    def get_timestamp(self):
        return self._timestamp

    def get_camera_data(self):
        if self._camera_data_raw is None:
            return None
        if self._camera_data is None:
            self._camera_data = CameraData.deserialise_as_png(self._camera_data_raw)
            self._camera_data.mask_cover()  # Always remove camera cover
        return self._camera_data

    def get_coordinates(self):
        if self._coordinates is None:
            self._coordinates = self._timestamp.to_location()
        return self._coordinates

    """Datasets"""

    def get_expected_ndvi(self):
        loc = self.get_coordinates()
        res = expected_ndvi.get(loc[0], loc[1])
        if (res is None) or (res > 1 or res < -1):
            return None  # Not possible
        return res

    def get_latitude(self):
        loc = self.get_coordinates()
        return loc[0]

    def get_land_cover(self):
        loc = self.get_coordinates()
        return land_cover.get(loc[0], loc[1])

    def get_population_density(self):
        loc = self.get_coordinates()
        return remove_none_or_negative(population_density.get(loc[0], loc[1]))

    def get_co2_emissions(self):
        loc = self.get_coordinates()
        return remove_none_or_negative(co2_emissions.get(loc[0], loc[1]))

    def get_historical_land_use(self):
        loc = self.get_coordinates()
        return historical_land_use.get(loc[0], loc[1])

    def get_gdp(self):
        loc = self.get_coordinates()
        return remove_none_or_negative(gdp.get(loc[0], loc[1]))

    def get_precipitation(self):
        loc = self.get_coordinates()
        return remove_none_or_negative(precipitation.get(loc[0], loc[1]))

    def get_temperature(self):
        loc = self.get_coordinates()
        return temperature.get(loc[0], loc[1])

    def get_radiation(self):
        loc = self.get_coordinates()
        return remove_none_or_negative(radiation.get(loc[0], loc[1]))

    def get_land_masked(self, to_mask: CameraData) -> np.array:
        """Return img to an array of values where this image is land, using the classifier Convolutional Neural Network inputted"""
        #
        # # Get classification mask
        # channels = self.get_camera_data().get_raw_channels()
        # classifier = Classifier(channels)
        # mask = classifier.predict_image()
        # #
        # # view_img = deepcopy(img)
        # # view_img.contrast()
        # # view_img.display()
        #
        # # # Debug - show masked image and ndvi
        # res = classifier.crop_to_tiles(deepcopy(self.get_camera_data().image))
        # res[np.logical_not(mask)] = res[np.logical_not(mask)] // 3
        # view_img = CameraData.from_processed_np_array(res)
        # view_img.display()
        # #
        # # demo_img = classifier.crop_to_tiles(deepcopy(img.image))
        # # demo_img[np.logical_not(mask)] = 0
        # # view_img = CameraData.from_processed_np_array(demo_img)
        # # view_img.contrast()
        # # view_img.display()

        # Get land mask - create URL for API
        long, lat = self.get_coordinates()
        width, height, _ = self.get_camera_data().image.shape
        scale_factor = max(width, height) / 640 # Won't display larger than 640x640 - mask size x sf = image size

        land_mask_url = f"https://maps.googleapis.com/maps/api/staticmap?center={long}," \
                        f"{lat}&zoom=7&format=png&size={height//scale_factor}x{width//scale_factor}&maptype=roadmap&style" \
                        f"=feature:administrative|visibility:off&style=feature:landscape|color:0x000000&style=feature" \
                        f":water|color:0xffffff&style=feature:road|visibility:off&style=feature:transit|visibility" \
                        f":off&style=feature:poi|visibility:off&key={GGLMAPS_KEY}"

        req = requests.get(land_mask_url, stream=True)

        print(land_mask_url)
        land_mask = np.asarray(bytearray(req.content), dtype=np.uint8) # Is sea
        land_mask = cv2.imdecode(land_mask, cv2.IMREAD_UNCHANGED)

        land_mask = cv2.resize(land_mask, (height, width))
        print(land_mask.shape)

        # img = self.get_camera_data()

        # cloud_mask = img.mask_lighter_total(310) # Cloud
        # print(np.sum(cloud_mask))

        mask = land_mask

        view_img = deepcopy(self.get_camera_data())
        view_img.image[land_mask] = 0
        view_img.display()

        return to_mask.image[mask]

    def get_ndvi(self):
        return self.get_camera_data().get_ndvi()

    def get_avg_ndvi(self):
        """Return the mean land ndvi of the datapoint, processed from images on the ISS"""
        if self._avg_ndvi is None:
            self._avg_ndvi = np.median(self.get_land_masked(self.get_ndvi()))
        return self._avg_ndvi

    def get_masked_ndvi_values(self):
        if self._masked_ndvi is None:
            self._masked_ndvi = self.get_land_masked(self.get_ndvi())
        return self._masked_ndvi

    def serialise(self):
        if self._timestamp is None:
            return {
                "lat": self._coordinates[0],
                "long": self._coordinates[1],
            }
        else:
            return {
                "timestamp": self._timestamp.serialise().hex(),
                "camera_data_raw": self._camera_data_raw.hex(),
                "ndvi": self._avg_ndvi
            }

    def deserialise(serialised):
        try:
            timestamp = TimeStampData.deserialise(
                bytes.fromhex(serialised["timestamp"])
            )
            camera_data_raw = serialised["camera_data_raw"]
            avg_ndvi = serialised["ndvi"] if "ndvi" in serialised else None # Try to get but otherwise return None
            return DataPoint.from_timestamp(
                timestamp,
                bytes.fromhex(camera_data_raw),
                avg_ndvi
            )
        # if no timestamp, don't panic!
        except:
            return DataPoint.from_coordinates((serialised["lat"], serialised["long"]))
