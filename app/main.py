import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Main page
@app.route('/')
def index():
    return render_template("index.html")

# Route for results page
@app.route('/results', methods=['POST'])
def results():
    uploaded_img = request.files['file']
    img_name = uploaded_img.filename

    # Saves image if something was uploaded
    if img_name != '':
        uploaded_img.save("images/" + img_name)
    
    # Do prediction stuff somewhere here

    
    return render_template('results.html', filename = img_name)

# Route for displaying image on the results page
@app.route('/upload/<img_name>')
def display_image(img_name):
    return send_from_directory("images", img_name)