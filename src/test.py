""" Script for testing POST request /w file classification """
from requests import post

# get file
TEST_PATH = "/Users/Erik/Dev/cordspot/data/test/test1.jpeg"

# create request and send it
res = post("http://127.0.0.1:5000/predict", files={"file": open(TEST_PATH, "rb")},)

print(res.json())
