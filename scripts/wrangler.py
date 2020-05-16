"""Wrangles images into neatly train/val sets of directories where each directory
contains train images XOR validation images from a label.

Images are rescaled in accordance with the targeted classifier (resnet in this case)
"""
# imports
import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import Image


# Raw data sourcing paths
IMAGE_FOLDER = "/Users/Erik/Dev/plugdetector/data/raw/images"  # label + uuid + ext
PROCESSED_PATH = "/Users/Erik/Dev/plugdetector/data/processed"  # => dir val / train

# setup training and validation folders with nested folders for each label
try:
    os.makedirs(os.path.join(PROCESSED_PATH, "train"))
except:
    print("Could not generate train directory. They probably already exist")
try:
    os.makedirs(os.path.join(PROCESSED_PATH, "val"))
except:
    print("Could not generate val directory. They probably already exist")

# get labels and their corresponding files
rawImagePaths = os.listdir(IMAGE_FOLDER)[1:]  # [0] == .DS_Datastore
labels = pd.Series(list(map(lambda path: path.split("-")[0], rawImagePaths))).unique()
labels_map = {}
for label in labels:
    labels_map[label] = pd.Series(rawImagePaths)[
        pd.Series(rawImagePaths).str.contains(label)
    ].tolist()


# Let's get some utility functions for showing resized images and their corres. class
import matplotlib as plt


def inspect(n, label):
    """Utlity function for inspecting n images (displaying them using matplotlib),
        their dimensions as well as their given label.

    Arguments:
        n {int} -- [description]

    Returns:
        [None] -- [description]
    """


# print(labels_map)
testImg1 = "/Users/Erik/Dev/plugdetector/data/test/iphone_charger-17c8b67c-017c-4731-9cbd-e62b2b2ed3e3.jpg"
testImg2 = "/Users/Erik/Dev/plugdetector/data/raw/images/power_female-060bb229-3ac2-4ada-8a0a-00c03edffd1a.jpg"
testImg3 = "/Users/Erik/Dev/plugdetector/data/raw/images/microphone_male-fae1c7f1-1e99-4bc8-942f-8f04014c9811.jpg"
# we want to go from (1080, 1920) to (300, 300)
img = Image.open(testImg3)
raw_height, raw_width = img.size
print(img.size)

img = img.resize(((raw_height) // 2, (raw_height) // 2,))
img.show()
print("print size after resize: ", img.size)

# Square image
def squarifyImage(image, axis="x"):
    raw_height, raw_width = img.size
    if resize
    return img.resize(((raw_height) // 2, (raw_height) // 2))
