# Contains utility functions for use in other packages
from uuid import uuid4 as uuid
import cv2 as cv
import random, os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


# util for generating valid file names containing uuid + class labels
def generateFrameFileName(label, extension=".jpg"):
    return f"{label}-" + str(uuid()) + extension


# Inspect a random subset of images from a given label
def inspectNLabeledImages(label, labeldict, image_folder, n=4):
    """Utility function for inspected an N subset of images denoted by a given label from a given folder.

    Arguments:
        label {string} -- String representation of the class label for a given image
        labeldict {dict} -- Dictionary containing a list of file references for each label (label: [filenames])
        image_folder {[string]} -- [Abs path to the source image folder]

    Keyword Arguments:
        n {int} -- [how many random samples to showed] (default: {4})
    """

    # Ensure that we can always get a square grid
    if n % 2 != 0:
        n += 1

    image_data = [
        cv.imread(os.path.join(image_folder, path))
        for path in random.sample(labeldict[label], n)
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
