# Contains utility functions for use in other packages
from uuid import uuid4 as uuid

# util for generating valid file names containing uuid + class labels
def generateFrameFileName(label, extension=".jpg"):
    return f"{label}-" + str(uuid()) + extension
