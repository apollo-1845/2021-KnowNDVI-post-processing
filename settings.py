#!/usr/bin/env python3
import os

IS_PROD = False

# Processing
PREFERRED_RESOLUTION = (1312, 976)
PREFERRED_RES_NP = (976, 1312)  # Reverse - for creating NumPy arrays

USE_PNG = True

# Output
OUT_DIR = os.path.join(".", "data")
OUT_FILE = os.path.join(OUT_DIR, "other", "out.blob")

# ISS Location - https://rhodesmill.org/skyfield/earth-satellites.html#loading-a-tle-set-from-strings and https://web.archive.org/web/20220505085514/http://www.celestrak.com/NORAD/elements/stations.txt
# As of May 05 2022 (to ensure accuracy)
ISS_TLE_1 = "1 25544U 98067A   22125.19210813  .00008001  00000+0  14831-3 0  9995"
ISS_TLE_2 = "2 25544  51.6431 189.5223 0006686  66.4371  32.9954 15.49937273338517"

# Classifier - Neural Network
CLASSIFIER_CROP_SIZE = 9  # 9px x 9px inputted
CLASSIFIER_TILE_SIZE = 5  # 5px x 5px squares on mask result - increase to speed up
CLASSIFIER_CERTAINTY_THRESHOLD = 0.5  # If more certain than this, land

# Land masking
# Add key from environment vars if possible, else prompt
if os.path.exists("data/private/gglmaps_key.txt"):
    with open("data/private/gglmaps_key.txt") as reader:
        GGLMAPS_KEY = reader.read()
else:
    GGLMAPS_KEY = input("Google Maps API Key:")
