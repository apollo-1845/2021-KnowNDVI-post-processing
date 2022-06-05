import os

import numpy as np
import cv2
from project_types import Data

from results.color_map import fastiecm

from settings import IS_PROD, USE_PNG, OUT_DIR


class CameraData(Data):
    """A photo taken from a camera, with methods to convert to NDVI."""

    image = None

    def is_invalid(self):
        """See if the data should not be recorded."""
        return self.image is None

    @staticmethod
    def from_processed_np_array(image):
        """Construct a CameraData object from processed data."""
        instance = CameraData()
        instance.image = image
        return instance

    def get_raw(self):
        """Get the raw data value stored in this wrapper."""
        return self.image

    def serialise(self) -> bytes:
        return self.serialise_as_png()

    def serialise_as_npz(self) -> bytes:
        """
        Return bytes that can be stored to represent the value.

        It can be done by representing the value as bytes or
        by serialising a file name with the data
        """
        if self.image is None and not IS_PROD:
            raise Exception("The image is None for CameraData serialisation")
        elif USE_PNG:
            return self.serialise_as_png()
        else:
            global save_id
            file_id = save_id
            np.savez_compressed(f"./out/cam_data_{file_id}.npz", data=self.image)

            save_id += 1  # Next image

            return int.to_bytes(
                file_id, length=(save_id.bit_length() + 7) // 8, byteorder="big"
            )

    @staticmethod
    def deserialise(b):
        return CameraData.deserialise_as_png(b)

    def deserialise_as_npz(b):
        """Reverse the serialisation process."""
        if USE_PNG:
            result = CameraData.deserialise_as_png(b)
            return result
        else:
            file_id = int.from_bytes(b, byteorder="big")
            out = CameraData()
            out.image = np.load(f"./out/cam_data_{file_id}.npz")["data"]
            return out

    def serialise_as_png(self) -> bytes:
        """Serialise the image data as a png."""
        global save_id
        # As PNG, return image ID
        image_id = save_id

        nir, vis = cv2.split(self.image)
        cv2.imwrite(os.path.join(OUT_DIR, "images", "nir", str(image_id) + "_nir.png"), nir)
        cv2.imwrite(os.path.join(OUT_DIR, "images", "vis", str(image_id) + "_vis.png"), vis)

        # Return as bytes; dynamic size based on size of image ID
        result = int.to_bytes(
            image_id, length=(image_id.bit_length() + 7) // 8, byteorder="big"
        )
        print("Serialised image file id", image_id)

        save_id += 1  # Next image
        return result

    @staticmethod
    def deserialise_as_png(b):
        """Deserialise the image data as a png."""
        # Load from bytes
        load_id = int.from_bytes(b, byteorder="big")
        # print("Deserialised image file id", load_id)
        # As PNG, get from ID
        nir = cv2.imread(os.path.join(OUT_DIR, "images", "nir", str(load_id) + "_nir.png"), \
                         cv2.IMREAD_ANYCOLOR)
        vis = cv2.imread(os.path.join(OUT_DIR, "images", "vis", str(load_id) + "_vis.png"), \
                         cv2.IMREAD_ANYCOLOR)

        img = np.dstack((nir, vis))

        return CameraData.from_processed_np_array(img)

    def __repr__(self):
        return f"📸(shape={self.image.shape})"

    def display(self):
        """Create a preview window of the contained image"""
        img = self.image.copy()

        # Fill the missing colour channel with zeroes so that it can be displayed properly
        if len(img.shape) == 3 and img.shape[2] == 2:

            print(img.shape, type(img[0][0][0]))

            # Handle NaN
            nir, vis = cv2.split(img)
            mask = nir == np.nan
            nir[mask] = 0
            vis[mask] = 0
            # Make renderable
            nir = nir.astype(np.uint8)
            vis = vis.astype(np.uint8)
            img = cv2.merge([nir, vis])

            print(img.shape)

            img = np.lib.pad(
                img, ((0, 0), (0, 0), (0, 1)), "constant", constant_values=(0)
            )
        elif len(img.shape) == 2:
            # One channel - apply color map
            img = cv2.applyColorMap(img.astype(np.uint8), fastiecm)

        # Display with cv2
        title = "Camera image preview"
        cv2.namedWindow(title)  # create window
        cv2.imshow(title, img)  # display image
        cv2.waitKey(0)  # wait for key press
        cv2.destroyAllWindows()

    """NDVI processing"""

    def get_ndvi(self):
        # Add contrast
        self.contrast()
        # Split into channels
        nir, vis = cv2.split(self.image)

        total = nir.astype(float) + vis.astype(float)
        total[total == 0] = 0.01  # Don't divide by zero!

        # More near-infrared and less visible reflected means plant
        ndvi = (nir.astype(float) - vis) / total

        # threshold = 0.18
        # ndvi[ndvi < threshold] = np.nan

        data = CameraData.from_processed_np_array(ndvi)
        # data.contrast()

        print(data)

        return data

    def mask_lighter_total(self, threshold: int):
        """Mask total NIR + VIS larger than threshold (up to 510)"""
        # Masking - total is the total of red and blue channels
        nir, vis = cv2.split(self.image)
        nir = nir.astype("float")  # NaN is a float
        vis = vis.astype("float")
        total = nir + vis

        mask = total > threshold
        nir[mask] = np.nan
        vis[mask] = np.nan
        self.image = cv2.merge([nir, vis])

    def mask_darker_total(self, threshold: int):
        """Mask total NIR + VIS smaller than threshold (up to 510)"""
        # Masking - total is the total of red and blue channels
        nir, vis = cv2.split(self.image)
        nir = nir.astype("float")  # NaN is a float
        vis = vis.astype("float")
        total = nir + vis

        mask = total < threshold
        nir[mask] = np.nan
        vis[mask] = np.nan
        self.image = cv2.merge([nir, vis])

    def mask_sea(self, threshold: float):
        """Mask where NIR^2:VIS > threshold"""
        # Masking - total is the total of red and blue channels
        nir, vis = cv2.split(self.image)
        nir = nir.astype("float")  # NaN is a float
        vis = vis.astype("float")

        vis[vis == 0] = 0.0001
        mask = (nir ** 2 / vis) > threshold
        nir[mask] = np.nan
        vis[mask] = np.nan
        self.image = cv2.merge([nir, vis])

    def get_unusable_area(self):
        nan_counts = np.count_nonzero(np.isnan(self.image))
        return nan_counts

    def get_mean_and_weight(self):
        # mean = mean pixel value, weight = how many valid pixels
        mean = np.nanmean(self.image)
        weight = len(self.image) - np.count_nonzero(
            np.isnan(self.image)
        )  # Pixels that aren't NaN

        return mean, weight

    def contrast(self):
        img = self.image

        # Get boundaries
        in_min = np.nanpercentile(img, 5)
        in_max = np.nanpercentile(img, 95)
        # print(in_min, in_max)
        out_min = 0.0
        out_max = 255.0
        # Stretch to boundaries
        result = img - in_min  # Now min is 0
        result *= (out_max - out_min) / (
            in_max - in_min
        )  # Divide away input range and then multiply in output range
        result += in_min  # N
        # now min is out_min m

        self.image = result
