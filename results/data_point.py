#!/usr/bin/env python
from copy import deepcopy

import cv2
import numpy as np

from classifier.predict import Classifier
from misc.dataset_reader import ASCReader
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData

landtype = ASCReader(
    "data/datasets/modis_landcover_class_qd.asc"
)  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png
# A helpful site for debugging: https://www.findlatitudeandlongitude.com/

class DataPoint:
    """A class representing a collection of available data for a certain timestamp and position"""

    def __init__(self, timestamp_data_raw, camera_data_raw):
        self._id = int.from_bytes(camera_data_raw, byteorder="big")
        self._timestamp_data_raw = timestamp_data_raw
        self._camera_data_raw = camera_data_raw

        self._timestamp = TimeStampData.deserialise(timestamp_data_raw)
        self._coordinates = None
        self._camera_data = None

    def get_id(self):
        return self._id

    def get_timestamp(self):
        return self._timestamp

    def get_camera_data(self):
        if self._camera_data is None:
            self._camera_data = CameraData.deserialise_as_png(self._camera_data_raw)
            self._camera_data.mask_cover() # Always remove camera cover
        return self._camera_data

    def get_coordinates(self):
        if self._coordinates is None:
            self._coordinates = self._timestamp.to_location()
        return self._coordinates

    def get_landtype(self):
        loc = self.get_coordinates()
        return landtype.get(loc[0], loc[1])

    def get_land_masked(self, model, img:CameraData) -> np.array:
        """Return img to an array of values where this image is land, using the classifier Convolutional Neural Network inputted"""
        # Get classification mask
        channels = self.get_camera_data().get_raw_channels()
        classifier = Classifier(channels, model)
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

    def serialise(self):
        return {
            "timestamp_data_raw": self._timestamp_data_raw.hex(),
            "camera_data_raw": self._camera_data_raw.hex(),
        }

    def deserialise(serialised):
        return DataPoint(
            bytes.fromhex(serialised["timestamp_data_raw"]),
            bytes.fromhex(serialised["camera_data_raw"]),
        )
