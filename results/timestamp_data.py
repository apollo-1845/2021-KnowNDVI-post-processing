#!/usr/bin/env python3
from time import time

from project_types import Data

import numpy as np

# ISS location
import datetime

from skyfield.api import EarthSatellite, load
from skyfield.timelib import utc
from skyfield.toposlib import wgs84
from settings import ISS_TLE_1, ISS_TLE_2

timescale = load.timescale()
iss = EarthSatellite(ISS_TLE_1, ISS_TLE_2, 'ISS', timescale)


class TimeStampData(Data):
    """A Data subclass that represents a timestamp."""

    data = None

    def is_invalid(self):
        """See if the data should not be recorded."""
        return self.data is None

    def __init__(self, _data):
        """Create a new instance."""
        self.data = _data

    def get_raw(self):
        """Get the raw data value stored in this wrapper."""
        return self.data

    def serialise(self) -> bytes:
        """Return bytes that can be stored to represent the value."""
        return self.data.tobytes()

    @staticmethod
    def deserialise(b):
        """Reverse the serialisation process."""
        return TimeStampData(np.frombuffer(b, dtype=np.uint64))

    def __repr__(self):
        return f"⌚{datetime.datetime.fromtimestamp(self.data[0])}"

    """Getting location"""

    def to_location(self):
        """Convert UNIX timestamp to ISS (lat, lon) location using skyfield"""
        date = datetime.datetime.fromtimestamp(self.data[0], tz=utc)
        # print(date)
        ts = timescale.from_datetime(date)
        geocentric = iss.at(ts)
        lat, lon = wgs84.latlon_of(geocentric)
        # print(lat.degrees, lon.degrees)
        return lat.degrees, lon.degrees  # Store in floating-point degrees
