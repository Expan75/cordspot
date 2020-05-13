"""
    This script transforms video files into correndonding images for a given framerate.
    The images are then exported to ../data/images
"""
# General imports
import cv2 as cv
import os
import numpy as np
import pandas as pd
from uuid import uuid4 as uuid

# PATH SETUP: abs for now... TODO: make relative
VIDEO_FOLDER = "/Users/Erik/Dev/plugdetector/data/raw/videos"
IMAGE_FOLDER = "/Users/Erik/Dev/plugdetector/data/raw/images"

# util function for formatting filename path
def formatPath(filename, action="load"):
    if action == "load":
        return os.path.join(VIDEO_FOLDER, filename)
    elif action == "save":
        return os.path.join(IMAGE_FOLDER, filename)


# util for generating valid file names containing uuid + class labels
def generateFrameFileName(label, extension=".jpg"):
    return f"{label}-" + str(uuid()) + extension


def videos2Frames(video_dir, image_dir):
    """Given a valid 

    Arguments:
        video_path {[string]} -- [abs. file path to video file to be chopped up]
        image_dir {[string]} -- [image_dir to write saved frames (as images) to]
    """
    # get filenames (NOTE: filenames == labels)
    full_video_names = os.listdir(VIDEO_FOLDER)
    try:
        full_video_names.remove(".DS_Store")  # MAC COMPATABILITY
    except:
        pass
    labels = [name.split(".")[0] for name in full_video_names]

    # Iteratively go through and process each video into a labeled image
    formattedFilePaths = list(
        map(lambda name: formatPath(name, action="load"), full_video_names)
    )

    def video2Frame(filepath):
        print(f"Capturing frames using {filepath}")
        vidcap = cv.VideoCapture(filepath)
        success, image = vidcap.read()

        while success:
            # video filmed by iphone6 are filed in 30fps / we only need 1 frame per sec
            filename = generateFrameFileName(labels[0], ".jpg")
            fullpath = os.path.join(IMAGE_FOLDER, filename)
            if not cv.imwrite(fullpath, image):
                raise Exception("Could not write frame as image")
            success, image = vidcap.read()
        return

    # Mine frames from videos
    for path in formattedFilePaths:
        video2Frame(path)

    return


# calls transform function
videos2Frames(VIDEO_FOLDER, IMAGE_FOLDER)

# As the image content does not shift dramatically per frame, we'll want to remove all but every n'th image
# MINOR FUNCTION TO REMOVE ALL EXCEPT EVERY N'th image goes here...


print("Finished script gracefully...")
