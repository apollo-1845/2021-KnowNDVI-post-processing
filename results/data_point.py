#!/usr/bin/env python
from copy import deepcopy

import cv2
import numpy as np

from classifier.predict import Classifier
from misc.dataset_reader import ASCReader
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData

landtype = ASCReader(
    "data/datasets/land_cover.asc"
)  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png
# A helpful site for debugging: https://www.findlatitudeandlongitude.com/
expected_ndvi = ASCReader("data/datasets/ndvi.asc")
population_density = ASCReader("data/datasets/population_density.asc")

artificial_data_point_id = 0


class DataPoint:
    """A class representing a collection of available data for a certain timestamp and position"""

    def __init__(self):
        self._coordinates = None
        self._camera_data = None
        self._masked_ndvi = None
        self._timestamp = None
        self._id = None
        self._camera_data_raw = None

    def from_timestamp(timestamp, camera_data_raw):
        out = DataPoint()
        out._id = int.from_bytes(camera_data_raw, byteorder="big")
        out._camera_data_raw = camera_data_raw

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

    def get_landtype(self):
        loc = self.get_coordinates()
        return landtype.get(loc[0], loc[1])

    def get_expected_ndvi(self):
        loc = self.get_coordinates()
        # a value of -77 represents data that is not useful
        out = expected_ndvi.get(loc[0], loc[1])
        if out is None or out <= -50:
            return None
        return out

    def get_population_density(self):
        loc = self.get_coordinates()
        out = population_density.get(loc[0], loc[1])
        if out is None or out < 0:
            return None
        return out

    def get_land_masked(self, img: CameraData) -> np.array:
        """Return img to an array of values where this image is land, using the classifier Convolutional Neural Network inputted"""
        # Get classification mask
        channels = self.get_camera_data().get_raw_channels()
        classifier = Classifier(channels)
        mask = classifier.predict_image()

        # Debug - show masked image and ndvi
        res = classifier.crop_to_tiles(deepcopy(self.get_camera_data().image))
        res[np.logical_not(mask)] = res[np.logical_not(mask)] // 3
        view_img = CameraData.from_processed_np_array(res)
        view_img.display()

        demo_img = classifier.crop_to_tiles(deepcopy(img.image))
        demo_img[np.logical_not(mask)] = 0
        view_img = CameraData.from_processed_np_array(demo_img)
        view_img.contrast()
        view_img.display()

        return classifier.crop_to_tiles(img.image)[mask]

    def get_ndvi(self):
        return self.get_camera_data().get_ndvi()

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
            }

    def deserialise(serialised):
        try:
            timestamp = TimeStampData.deserialise(
                bytes.fromhex(serialised["timestamp"])
            )
            camera_data_raw = serialised["camera_data_raw"]
            return DataPoint.from_timestamp(
                timestamp,
                bytes.fromhex(camera_data_raw),
            )
        # if no timestamp, don't panic!
        except:
            return DataPoint.from_coordinates((serialised["lat"], serialised["long"]))
