import os
from flask import Flask, render_template, request, abort
from io import BytesIO
from PIL import Image
import base64
import json
import random
from .predictImage import predictImage

# Fetching facts from json
with open('flask_app/facts.json') as f:
  facts = json.load(f)

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

    # Checks for the filetype of the file uploaded
    if img_name != "":
        file_ext = os.path.splitext(img_name)[1]
        
        # Checks for file extensions
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(415) # Unsorported media type
    else:
        return render_template("index.html")

    im = Image.open(uploaded_img)
    im = im.convert("RGB")

    # Do prediction stuff starting from here
    # pred_tables = tuple of three strings
    # pred_scores = tuple of three floats
    pred_labels, pred_scores = predictImage(im)

    # Generate random number
    rand_num = random.randint(0,2)

    # For rendering image
    data = BytesIO()
    im.save(data, "PNG")    # Saves image in-memory, no need to save it into a folder.
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template(
        "results.html", 
        img_data = encoded_img_data.decode('utf-8'),
        fact_string = facts[pred_labels[0]][rand_num],
        pred_label = pred_labels,
        pred_score = pred_scores
    )

