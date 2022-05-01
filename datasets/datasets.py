import urllib.parse
from io import BytesIO

import requests
from PIL import Image # TODO: Update to OpenCV


class Dataset:
    """Class for retrieving data from NASA's datasets for comparison with PIR plant health data - All API_ prefixed methods access the STAC REST API to return default structures, and other methods convert this into usable data. - we need to be very cautious about efficiency here"""
    def __init__(self, url:str, collections:list):
        """Create a dataset from a STAC API (https://stacspec.org/STAC-api.html) endpoint (please leave a trailing / at the end so url-concatenation works) and a list of collections to search."""
        self.URL = url
        self.search_URL = urllib.parse.urljoin(self.URL, "search")
        print(self.URL, self.search_URL)
        self.collections = collections

    def API_search(self, bbox:list, datetime:str, page:int=1):
        """Search for features from the API that are in the bounding box and return them as a dictionary JSON structure (https://stacspec.org/STAC-api.html#operation/postSearchSTAC)"""
        results = requests.post(url=self.search_URL, json={
            "bbox": bbox,
            "datetime": datetime,
            "collections": self.collections,
            "page": page
        })
        return results.json()

    def get_features(self, bbox:list, datetime:str):
        """Generator function for retrieving features from the API"""
        response = self.API_search(bbox, datetime)
        for feature in response["features"]:
            yield Feature(feature)

class Feature:
    """Lightweight class for retrieving assets and information about a feature"""
    def __init__(self, feature):
        """Initialize a Feature instance from a JSON dictionary"""
        self.feature = feature

    def process_asset(self, name:str, process:callable):
        """Get an asset by name as a PIL Image, and process it using a function argument"""
        image_href = self.feature["assets"][name]["href"]
        image_resp = requests.get(image_href)
        image = BytesIO(image_resp.content)
        with Image.open(image) as img:
            return process(img)