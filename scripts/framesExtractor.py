"""
    This script transforms video files into correndonding images for a given framerate.
    The images are then exported to ../data/images
"""
# General imports
import cv2 as cv
import os
from uuid import uuid4 as uuid

# PATH SETUP: abs for now... TODO: make relative
VIDEO_FOLDER = "/Users/Erik/Dev/cordspot/data/raw/videos"
IMAGE_FOLDER = "/Users/Erik/Dev/cordspot/data/raw/images"

# util function for formatting filename path
def formatPath(filename, action="load"):
    if action == "load":
        return os.path.join(VIDEO_FOLDER, filename)
    elif action == "save":
        return os.path.join(IMAGE_FOLDER, filename)


# util for generating valid file names containing uuid + class labels
def generateFrameFileName(label, extension=".jpeg"):
    return f"{label}-" + str(uuid()) + extension


def videos2Frames(video_dir, image_dir, nth_frame=30):
    """Given a video directory and valid format videoss within it, translates each videos' frames as images
    into an image dir, ensuring each photo is labeled and given an uuid. Returns blank.

    Arguments:
        video_path {[string]} -- [abs. file path to video file to be chopped up]
        image_dir {[string]} -- [image_dir to write saved frames (as images) to]
    """
    # get labels (filenames) (NOTE: filenames == labels)
    full_video_names = os.listdir(VIDEO_FOLDER)
    try:
        full_video_names.remove(".DS_Store")  # MAC COMPATABILITY
    except:
        pass

    labels = [name.split(".")[0] for name in full_video_names]
    # Iteratively go through and process each video into a labeled image
    formattedVideoFilePaths = [
        formatPath(name, action="load") for name in full_video_names
    ]

    def video2Frame(filepath, label):
        print(f"Capturing frames using {filepath}")
        vidcap = cv.VideoCapture(filepath)
        success, image = vidcap.read()

        imgPaths = []

        while success:
            # video filmed by iphone6 are filed in 30fps (no big difference from frame to frame => bias)
            filename = generateFrameFileName(label, ".jpeg")
            fullpath = os.path.join(IMAGE_FOLDER, filename)
            imgPaths.append(fullpath)
            if not cv.imwrite(fullpath, image):
                raise Exception("Could not write frame as image")
            success, image = vidcap.read()

        return label, imgPaths

    # Delete nth frames if given
    def keepEveryNthFrame(absfilepaths, nth):
        """Removes every nth file in a list of files

        Arguments:
            absfilepaths {[strings]} -- [abs paths to delete files at]
            nth {int} -- [removes all but this picture]
        """

        filesToKeep = []
        for file in absfilepaths[::nth]:
            filesToKeep.append(file)

        for file in absfilepaths:
            if file not in filesToKeep:
                ### Security: ensure we ONLY can delete .jpgs
                try:
                    os.remove(file)

                except OSError as error:
                    print(f"ERROR: could not remove {file}")
            else:
                continue
        print("successfully removed all but every %i frame." % nth)
        return

    meta = {}
    # Mine frames from videos
    for path, label in zip(formattedVideoFilePaths, labels):
        label, imgPaths = video2Frame(path, label)
        print(label, imgPaths)
        meta[label] = imgPaths

    # Delete every nth if desired
    if (nth_frame != 0) & (type(nth_frame) == int):
        # Go through each classes files
        for label in meta.keys():
            keepEveryNthFrame(meta[label], nth_frame)
    else:
        print("ERROR: Please provide a valid argument for how frames to keep.")
        return

    return


# calls transform function
videos2Frames(VIDEO_FOLDER, IMAGE_FOLDER, nth_frame=60)


print("Finished script gracefully...")
