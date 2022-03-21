import numpy as np
import cv2


def write_to_file(file_path_with_dir, content):
    f1 = open(file_path_with_dir, "w+")
    f1.write(content)
    f1.close


def prepare_input_for_demographic(img):
    # Function to normalise the input to the model.

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image_data_flat = img.shape[0] * img.shape[1]
    if image_data_flat > 120 * 60:
        img = cv2.resize(img, (60, 120), cv2.INTER_AREA)
    else:
        img = cv2.resize(img, (60, 120), cv2.INTER_LINEAR)

    img = np.expand_dims(img, axis=0)
    return img
