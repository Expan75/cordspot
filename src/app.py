from flask import Flask

app = Flask(__name__)


### Basic routes
@app.route("/health")
def health_check():
    return "We're alive!"


@app.route("/")
def hello_world():
    return "Hello, World!"
