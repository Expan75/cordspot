"""Wrangles images into neatly train/val sets of directories where each directory
contains train images XOR validation images from a label.

Images are rescaled in accordance with the targeted classifier (resnet in this case)
"""
# imports
import os
import cv2 as cv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import Image

# Let's get some utility functions for showing resized images and their corres. class
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import random


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


# get labels and their corresponding files; TODO: encapsulate into reusuable function
rawImagePaths = os.listdir(IMAGE_FOLDER)[1:]  # [0] == .DS_Datastore
labels = pd.Series(list(map(lambda path: path.split("-")[0], rawImagePaths))).unique()
labels_map = {}
for label in labels:
    labels_map[label] = pd.Series(rawImagePaths)[
        pd.Series(rawImagePaths).str.contains(label)
    ].tolist()


# Square image TODO: fix and incorperate into pipeline
def squarifyImage(image, axis="x"):
    raw_height, raw_width, channels = image.shape
    size = raw_width if axis.lower() else raw_height
    return image.resize(((size) // 2, (size) // 2))


# Inspect a random subset of images from a given label
def inspectNLabeledImages(label, labeldict, n=4, image_folder=IMAGE_FOLDER):
    """Utility function for inspected an N subset of images denoted by a given label from a given folder.

    Arguments:
        label {string} -- String representation of the class label for a given image
        labeldict {dict} -- Dictionary containing a list of file references for each label (label: [filenames])

    Keyword Arguments:
        n {int} -- [how many random samples to showed] (default: {4})
        image_folder {[string]} -- [Abs path to the source image folder] (default: {IMAGE_FOLDER})
    """

    # Ensure that we can always get a square grid
    if n % 2 != 0:
        n += 1

    image_data = [
        cv.imread(os.path.join(image_folder, path))
        for path in random.sample(labels_map[label], n)
    ]

    fig = plt.figure(figsize=(10.0, 6.0))
    fig.suptitle(label)
    grid = ImageGrid(
        fig,
        111,  # similar to subplot(111)
        nrows_ncols=(2, 2),  # creates 2x2 grid of axes
        axes_pad=0.1,  # pad between axes in inch.
    )

    for ax, im in zip(grid, image_data):
        # Iterating over the grid returns the Axes.
        ax.imshow(im)

    plt.show()

    return


# OUTPUT ALL LABELS
# for label in labels:
#     print(label)

# Inspect a random subset of each class
# for label in labels:
#     inspectNLabeledImages(label, labels_map)
