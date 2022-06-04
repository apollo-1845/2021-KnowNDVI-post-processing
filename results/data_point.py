#!/usr/bin/env python
from results.camera_data import CameraData
from results.timestamp_data import TimeStampData

landtype = ASCReader(
    "data/datasets/modis_landcover_class_qd.asc"
)  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png


class DataPoint:
    """A class representing a collection of available data for a certain timestamp and position"""

    def __init__(self, timestamp_data_raw, camera_data_raw):
        self._timestamp = TimeStampData.deserialise(timestamp_data_raw)
        self._camera_data_raw = camera_data_raw
        self._coordinates = self._timestamp.to_location()
        self._camera_data = None

    def get_timestamp(self):
        return self._timestamp

    def get_camera_data(self):
        if self._camera_data == None:
            self._camera_data = CameraData.deserialise_as_png(self._camera_data_raw)
        return self._camera_data

    def get_coordinates(self):
        return self._coordinates

    def get_landtype(self):
        landtype.get(loc[0], loc[1])
