import cv2
import numpy as np
import requests

from settings import GGLMAPS_KEY


def zoom_sea_mask(sea_mask, zoom_factor):
    """Rescale a mask by the specified scale factor around its central point"""
    old_hheight = int(sea_mask.shape[0] // 2)
    old_hwidth = int(sea_mask.shape[1] // 2)
    new_hheight = int(old_hheight // zoom_factor)
    new_hwidth = int(old_hwidth // zoom_factor)
    # Get slice
    return sea_mask[old_hheight-new_hheight:old_hheight+new_hheight, old_hwidth-new_hwidth:old_hwidth+new_hwidth]


def get_sea_mask(long:float, lat:float, width:int, height:int):
    """Get a sea mask from Google Maps"""
    api_scale_factor = max(width, height) / 640  # Won't display larger than 640x640 - mask size x sf = image size

    sea_mask_url = f"https://maps.googleapis.com/maps/api/staticmap?center={long}," \
                   f"{lat}&zoom=6&format=png&size={int(height // api_scale_factor)}x{int(width // api_scale_factor)}&maptype=roadmap&style" \
                   f"=feature:administrative|visibility:off&style=feature:landscape|color:0x000000&style=feature" \
                   f":water|color:0xffffff&style=feature:road|visibility:off&style=feature:transit|visibility" \
                   f":off&style=feature:poi|visibility:off&key={GGLMAPS_KEY}"

    resp = requests.get(sea_mask_url, stream=True)

    print(sea_mask_url)
    sea_mask = np.asarray(bytearray(resp.content), dtype=np.uint8)
    sea_mask = cv2.imdecode(sea_mask, cv2.IMREAD_UNCHANGED)  # Is sea

    try:
        sea_mask, _, _ = cv2.split(sea_mask)  # 1 channel
    except Exception:
        raise ValueError("Correct image size not returned because: " + resp.text)

    # Matrix rotate + translate + scale
    # IMG670 - dynamic using skyfield next
    trans_x = -144 #-127
    trans_y = -63 #-52
    rot_angle = 174.3
    zoom_factor = 1.8 # 2.07

    sea_mask = zoom_sea_mask(sea_mask, zoom_factor)

    # Resize to size of viewport
    sea_mask = cv2.resize(sea_mask, (height, width))

    rows, cols = sea_mask.shape
    rot_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rot_angle, 1)
    trans_matrix = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
    sea_mask = cv2.warpAffine(sea_mask, rot_matrix, (cols, rows))
    sea_mask = cv2.warpAffine(sea_mask, trans_matrix, (cols, rows))

    sea_mask = (sea_mask != 0)

    return sea_mask