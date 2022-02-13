#!/usr/bin/env python3
import os

IS_PROD = False

# Processing
PREFERRED_RESOLUTION = (640, 480)
PREFERRED_RES_NP = (480, 640)  # Reverse - for creating NumPy arrays

USE_PNG = True

# Output
OUT_DIR = os.path.join(".", "out")
OUT_FILE = os.path.join(OUT_DIR, "out.blob")
