# Main imports
from flask import Flask, jsonify, request

# Rel. Modules
from .inference import get_prediction

# Boilerplate setup
app = Flask(__name__)


""" ---- ROUTES ---- """
# Health Route
@app.route("/")
def health_check():
    return "Beep. Boop."


# Main predict route
@app.route("/predict", methods=["POST"])
def predict():

    if request.method == "POST":
        # we will get the file from the request
        file = request.files["file"]

        # Handle null image
        if file.filename == "":
            return jsonify("Error: please provide an image")
        else:
            # convert that to bytes
            img_bytes = file.read()
            class_id, class_name = get_prediction(image_bytes=img_bytes)
            return jsonify({"class_id": class_id, "class_name": class_name})


""" ---- END OF ROUTES ---- """


if __name__ == "__main__":
    app.run()
