import os
from flask import Flask, render_template, request, abort, flash
import io
from PIL import Image
import base64


app = Flask(__name__)

# Uploads can only be up to 15MB, this is checked automatically
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

# Image types that can be accepted
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".webp"]

# Main page
@app.route("/")
def index():
    return render_template("index.html")

# Route for results page
@app.route("/", methods=['POST'])
def results():
    uploaded_img = request.files["file"]
    img_name = uploaded_img.filename

    # Saves image if something was uploaded
    if img_name != "":
        file_ext = os.path.splitext(img_name)[1]
        
        # Checks for file extensions
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(415) # Unsorported media type
    else:
        return render_template("index.html")

    im = Image.open(uploaded_img)

    # Do prediction stuff starting from here
    # image_data = np.asarray(image).copy() # Equivalent to imread(image_file)

    # For rendering image
    data = io.BytesIO()
    im.save(data, "PNG")    # Saves image in-memory, no need to save it into a folder.
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("results.html", img_data = encoded_img_data.decode('utf-8'))