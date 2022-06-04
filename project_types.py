#!/usr/bin/env python3
from abc import ABC, abstractmethod


class Data(ABC):
    """An abstract class that represents a piece of data produced by a sensor."""

    @abstractmethod
    def is_invalid(self):
        """See if the data should not be recorded."""
        pass

    @abstractmethod
    def get_raw(self):
        """Get the raw data value stored in this wrapper."""
        pass

    @abstractmethod
    def serialise(self) -> bytes:
        """
        Return bytes that can be stored to represent the value.

        It can be done by representing the value as bytes or
        by serialising a file name with the data
        """
        pass

    @staticmethod
    @abstractmethod
    def deserialise(b: bytes):
        """Reverse the serialisation process."""
        pass


class Sensor(ABC):
    """An abstract class that represents a sensor that can return a data object."""

    @abstractmethod
    def capture_data(self):
        """Record some value and return a subclass of Data containing that value."""
        pass


class DataPoint:
    """A class representing a collection of available data for a certain timestamp and position"""

    def __init__(self, timestamp, image):
        self.timestamp = timestamp
        self.image = image

    def __repr__(self):
        return f"@[{self.timestamp}]: [{self.image}]"
