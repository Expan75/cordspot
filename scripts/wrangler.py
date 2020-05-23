"""Wrangles images into neatly train/val sets of directories where each directory
contains train images XOR validation images from a label.

Images are rescaled in accordance with the targeted classifier (resnet in this case)
"""
# imports
import random
import os
import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.axes_grid1 import ImageGrid
from sklearn.model_selection import train_test_split

# utility functions for inspecting image i/o
from utils import generateFrameFileName, inspectNLabeledImages

# System
MAC_OS = True

# Raw data sourcing paths
IMAGE_FOLDER = "/Users/Erik/Dev/plugdetector/data/raw/images"  # label + uuid + ext
PROCESSED_PATH = "/Users/Erik/Dev/plugdetector/data/processed"  # => dir val / train
TEST_PATH = "/Users/Erik/Dev/plugdetector/data/test"

# Create train and validation folders inside proccessed
for name in ["train", "valid"]:
    try:
        os.mkdir(os.path.join(PROCESSED_PATH, name))
    except FileExistsError:
        print("Could not create %s folder as it exists." % name)


# get labels and their corresponding files; TODO: encapsulate into reusuable function
rawImagePaths = os.listdir(IMAGE_FOLDER)[
    int(MAC_OS) :
]  # [0] == .DS_Datastore on mac systems
labels = pd.Series(list(map(lambda path: path.split("-")[0], rawImagePaths))).unique()

labels_map = {}
for label in labels:
    labels_map[label] = pd.Series(rawImagePaths)[
        pd.Series(rawImagePaths).str.contains(label)
    ].tolist()
    # print(label)


# Inspect a random subset of each class
# for label in labels:
#     inspectNLabeledImages(label, labels_map)


# test_path = os.path.join(
#     "/Users/Erik/Dev/plugdetector/data/test",
#     "iphone_charger-17c8b67c-017c-4731-9cbd-e62b2b2ed3e3.jpg",
# )


def grayscale(img):
    """Returns img as grayscaled"""
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def squareCrop(img):
    """Returns img cropped by the smallest axis (to make it square) """
    new_size = (min(img.shape), min(img.shape))
    return cv.resize(img, new_size)


def imagePipeline(img):
    """Composes transformers into a pipeline that can be applied to multiple images.
    Takes in a raw (opened) image and returns the square, grayscaled, and downsampled equiv.
    Arguments

    Arguments:
        img {[ndarray]} -- [description]
        shape {[tuple]} -- [tuple of the desired 2D dimensions of the final image]

    Returns:
        [cv.image] -- [numpy.Array]
    """
    gray = grayscale(img)
    square = squareCrop(gray)

    new_dims = tuple([dim // 4 for dim in square.shape])
    final_image = cv.resize(square, (new_dims))

    return final_image


def writeTransform(imageSet, train=True):
    """Transforms and writes images to either the train or validation folder

    Arguments:
        imageSet {list} -- [full paths for each image file]

    Keyword Arguments:
        train {bool} -- [description] (default: {True})
    """

    # set the target dir dep. if it is a training or validation set
    if train:
        save_folder = os.path.join(PROCESSED_PATH, "train")
    else:
        save_folder = os.path.join(PROCESSED_PATH, "valid")

    # Get corresponding labels and create sub folders for each
    labels = pd.Series(list(map(lambda path: path.split("-")[0], imageSet)))
    for label in labels.unique():
        try:
            os.mkdir(os.path.join(save_folder, label))
        except FileExistsError:
            print("Could not create %s folder as it exists." % label)

    # Save into corresponding folder
    for label, image in zip(labels, imageSet):
        # Transform image
        old_image_path = os.path.join(IMAGE_FOLDER, image)
        new_image = imagePipeline(cv.imread(old_image_path))
        # Save
        folder = os.path.join(save_folder, label)
        fullpath = os.path.join(folder, image)
        cv.imwrite(fullpath, new_image)

    return
# 1: Get data neatly ordered
pairs = []
for label in labels_map:
    for path in labels_map[label]:
        data = (label, path)
        pairs.append(data)

df = pd.DataFrame(data=pairs, columns=["label", "image"])
x, y = df.image, df.label

# 2: train test split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.15, random_state=42
)




# transform and write train set
writeTransform(x_train, train=True)

# transform and write valid set
writeTransform(x_test, train=False)
