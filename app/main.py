import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, after_this_request, abort

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
        uploaded_img.save("images/" + img_name)
        file_ext = os.path.splitext(img_name)[1]
        
        # Checks for file extensions
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            os.remove("images/" + img_name)
            abort(415) # Unsorported media type
    
    # Do prediction stuff somewhere here


    return render_template("results.html", filename = img_name)

# Route for displaying image on the results page
@app.route("/upload/<img_name>")
def display_image(img_name):

    # Delete file immediately after the page has been rendered
    @after_this_request
    def remove_file(response):
        os.remove("images/" + img_name)
        return response
        
    return send_from_directory("images", img_name)