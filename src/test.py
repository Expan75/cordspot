""" Script for testing POST request /w file classification """
from requests import post
import os

# get files
TEST_PATH = "/Users/Erik/Dev/cordspot/data/test"
subfolders = os.listdir(TEST_PATH)
for label in subfolders:
    # run predict on each file in them
    label_path = os.path.join(TEST_PATH, label)
    image_paths = [
        os.path.join(label_path, relpath) for relpath in os.listdir(label_path)
    ]
    print("Running predict on %s" % label)
    for image in image_paths:
        res = post("http://127.0.0.1:5000/predict", files={"file": open(image, "rb")},)
        print(res.text)

# output
# print(res.json())
