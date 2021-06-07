import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" 

from flask import Flask, render_template, request, abort
from io import BytesIO
from PIL import Image
import base64
import json
import random
import requests
from tensorflow.keras.models import model_from_json
from .predictImage import predictImage

# Load model
with open('flask_app/model/xception_model.json', 'r') as f:
    model_json = f.read()

model = model_from_json(model_json)

# Add weights
model.load_weights('flask_app/model/xception_weights.h5')

# Array of labels
labels = [
    "Alley", "Bridge", "Canyon", "Desert", "Downtown", 
    "Forest", "Grotto", "Iceberg", "Lake", "Mountain", 
    "Ocean", "Park", "Rock Arch", "Ruin", "Sky", 
    "Snowfield", "Street", "Tower", "Village", "Waterfall"
]

# Fetching facts from json
with open('flask_app/facts.json') as f:
  facts = json.load(f)

# Initiating Flask app
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
    if request.form["img_link"] == "":
        uploaded_img = request.files["file"]
        img_name = uploaded_img.filename

        # Checks for the filetype of the file uploaded
        if img_name != "":
            file_ext = os.path.splitext(img_name)[1]
            
            # Checks for file extensions
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template("index.html")
        else:
            return render_template("index.html")

        im = Image.open(uploaded_img)
    
    else:
        url = request.form["img_link"]
        try:
            response = requests.get(url)
        except:
            return render_template("index.html")
        im = Image.open(BytesIO(response.content))
    
    im = im.convert("RGB")

    labels_copy = labels.copy()

    # Do prediction stuff starting from here
    # pred_tables = tuple of three strings
    # pred_scores = tuple of three floats
    pred_labels, pred_scores = predictImage(model, labels_copy, im)

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

