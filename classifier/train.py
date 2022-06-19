"""Train the neural network"""
import cv2
import tensorflow as tf
import numpy as np

from settings import CLASSIFIER_CROP_SIZE

# We used this code to train the classification NN on Google Colab,
# then zipped and downloaded the saved model to `data/classifier/model`.
# This ensured that we only had to train the model once, and had Colab's
# quicker GPU speeds.

# The inputs we gave the model were the surrounding neighbourhood of
# each pixel in NIR, visible light and NDVI values. This was passed
# through a convolutional neural network to give a certainty that
# the central pixel was land. We then used a threshold to gain a
# boolean mask of land. (please see `predict.py`)


"""Create the model"""

# NN
model = tf.keras.models.Sequential([
    # Convolutions
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(9, 9, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(9, 9, 3)),
    # Main neurons
    tf.keras.layers.Flatten(),  # 243
    tf.keras.layers.Dense(500, activation='relu'),  # 5x5 grid with 2 layers (NIR, VIS)
    tf.keras.layers.Dense(1, activation='sigmoid')  # Output: is cloud?
])

model.compile(optimizer="adam",
              loss='binary_crossentropy',  # Boolean output
              metrics=['accuracy'], run_eagerly=True)

"""Process inputs: crop-creating functions"""

CROP_SIZE = CLASSIFIER_CROP_SIZE
PIXELS_TO_CENTRE = CROP_SIZE // 2
PIXELS_TO_CENTRE_2 = CROP_SIZE - PIXELS_TO_CENTRE

training_images = []  # Array of NIR then VIS
training_labels = []  # 1 for discard, 0 otherwise


def create_empty_col(length):
    """Create a line of zeros all in a 1-item array of len length"""
    return np.zeros(length)


def create_empty_row(length):
    """Create a line of zeros each in a 1-item array of len length"""
    return np.array([np.array([0]) for x in range(length)])


def get_crop(nir: np.array, vis: np.array, ndvi: np.array, x: int, y: int, CROP_SIZE: int, PIXELS_TO_CENTRE: int,
             PIXELS_TO_CENTRE_2: int):
    """Get the cropped portion of the image from nir and vis"""
    start_y = y - PIXELS_TO_CENTRE
    end_y = y + PIXELS_TO_CENTRE_2
    start_x = x - PIXELS_TO_CENTRE
    end_x = x + PIXELS_TO_CENTRE_2

    height = nir.shape[0]
    width = nir.shape[1]

    nir_crop = nir[start_y:end_y, start_x:end_x]
    vis_crop = vis[start_y:end_y, start_x:end_x]
    ndvi_crop = ndvi[start_y:end_y, start_x:end_x]

    if (start_y < 0):
        for i in range(CROP_SIZE - nir_crop.shape[0]):
            empty_line = create_empty_col(nir_crop.shape[1])  # Width
            nir_crop = np.vstack([empty_line, nir_crop])  # Vertical, before
            vis_crop = np.vstack([empty_line, vis_crop])  # Vertical, before
            ndvi_crop = np.vstack([empty_line, ndvi_crop])  # Vertical, before
        # print("-y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
    elif (end_y > height):
        for i in range(CROP_SIZE - nir_crop.shape[0]):
            empty_line = create_empty_col(nir_crop.shape[1])  # Width
            nir_crop = np.vstack([nir_crop, empty_line])  # Vertical, after
            vis_crop = np.vstack([vis_crop, empty_line])  # Vertical, after
            ndvi_crop = np.vstack([ndvi_crop, empty_line])  # Vertical, after
        # print("+y>", nir_crop.shape, vis_crop.shape, start_x, start_y)
    if (start_x < 0):
        for i in range(CROP_SIZE - nir_crop.shape[1]):
            empty_line = create_empty_row(nir_crop.shape[0])  # Height
            nir_crop = np.hstack([empty_line, nir_crop])  # Horizontal, before
            vis_crop = np.hstack([empty_line, vis_crop])  # Horizontal, before
            ndvi_crop = np.hstack([empty_line, ndvi_crop])  # Horizontal, before
            # print(nir_crop)
        # print("-x>", nir_crop.shape, vis_crop.shape, start_x, start_y)
    elif (end_x > width):
        for i in range(CROP_SIZE - nir_crop.shape[1]):
            empty_line = create_empty_row(nir_crop.shape[0])  # Height
            nir_crop = np.hstack([nir_crop, empty_line])  # Horizontal, after
            vis_crop = np.hstack([vis_crop, empty_line])  # Horizontal, after
            ndvi_crop = np.hstack([ndvi_crop, empty_line])  # Horizontal, after
        # print("+x>", nir_crop.shape, vis_crop.shape, start_x, start_y)

    return nir_crop.astype(float), vis_crop.astype(float), ndvi_crop


def get_training_crops(nir: np.array, vis: np.array, ndvi: np.array, mask: np.array, min_x: int, min_y: int,
                       crop_size: int):
    """Return the training_images and training_labels lists updated to include the new crops"""
    pixels_to_centre = crop_size // 2
    pixels_to_centre_2 = crop_size - pixels_to_centre

    # Get max x + y
    max_x = min_x + mask.shape[1]  # height, width
    max_y = min_y + mask.shape[0]  # height, width

    training_images = []
    training_labels = []

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):

            is_land = mask[y - min_y, x - min_x] == 255  # If 255, then land
            if (is_land or (x % 3 != 0 and y % 3 != 0)):
                # if(not is_land): print(x, y)
                # More land crops

                nir_crop, vis_crop, ndvi_crop = get_crop(nir, vis, ndvi, x, y, crop_size, pixels_to_centre,
                                                         pixels_to_centre_2)
                # print(nir_crop.shape, vis_crop.shape, start_x, start_y)

                # if (nir_crop.shape != (5, 5)):
                #   print(nir_crop.shape)

                if (np.sum(vis_crop) != 0):
                    # if(is_land): print(x, y, int(is_land))
                    # print(vis_crop*255)
                    # print(is_land)
                    # print([nir_crop.dtype, vis_crop.dtype, ndvi_crop.dtype])
                    training_images.append(np.array(cv2.merge([nir_crop, vis_crop, ndvi_crop])))
                    training_labels.append(int(is_land))

    return training_images, training_labels

"""Process inputs: mask processing functions"""

def get_ndvi(nir: np.array, vis: np.array):
    total = (nir.astype(float) + vis.astype(float))
    total[total == 0] = 0.0001  # no DivBy0
    ndvi = (nir.astype(float) - vis) / total
    print(np.nan in ndvi, np.inf in ndvi)
    return ndvi

def train_with_mask(training_images, training_labels, img_id: int, x=0, y=0, width=None, height=None):
    """Train the model with a (section of a) photo with *a mask in the training folder* by placing them into the training images and labels buffers"""
    print("Getting data for image", img_id)
    # Get nir, vis and ndvi
    nir = cv2.imread(f"classifier_training/{img_id}_nir.png")
    nir, _, _ = cv2.split(nir)  # Extract 1 channel and crop; discard other 2
    vis = cv2.imread(f"classifier_training/{img_id}_vis.png")
    vis, _, _ = cv2.split(vis)  # Extract 1 channel; discard other 2
    # Get mask
    mask = cv2.imread(f"classifier_training/{img_id}_mask.png")
    mask, _, _ = cv2.split(mask)  # Extract 1 channel; discard other 2

    if (width is None): width = mask.shape[1]
    if (height is None): height = mask.shape[0]

    nir = nir[y:y + height, x:x + width]
    vis = vis[y:y + height, x:x + width]
    ndvi = get_ndvi(nir, vis)

    training_images_temp, training_labels_temp = get_training_crops(nir, vis, ndvi, mask, x, y, CROP_SIZE)
    training_images.extend(training_images_temp)
    training_labels.extend(training_labels_temp)
    print(len(training_images), "images")

"""Process inputs: high-level"""
training_images = []
training_labels = []

train_with_mask(training_images, training_labels, 540)
train_with_mask(training_images, training_labels, 670)
train_with_mask(training_images, training_labels, 1865)

# Convert to np
training_images = np.array(training_images)
training_labels = np.array(training_labels)

print(f"{training_labels.sum()} / {len(training_labels)} land")

"""Training and saving the model"""
model.fit(training_images, training_labels, epochs=3)
model.save("data/classifier/model_temp") # Copy this into model if it is the one we are using.