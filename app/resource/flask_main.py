# importing required libraries
import os
from flask import Blueprint
from flask import flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from app import app

# importing helper functions
from app.service.Main import ObjectDetector, StoreImage, RetrieveImages

flask_main_app = Blueprint('main_app', __name__)  # creating Blueprint for flask app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # file extensions supported for our app


# function to check is file valid or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# rendering index.html on homepage of app
@flask_main_app.route('/')
def homepage():
    return render_template('index.html')


# rendering upload.html for uploading images
@flask_main_app.route('/upload')
def upload_form():
    return render_template('upload.html')


# uploading and saving image
@flask_main_app.route('/upload', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []  # it will store all files uploaded
    for file in files:
        if file and allowed_file(file.filename):  # checking for allowed file
            filename = secure_filename(file.filename)
            file_names.append(filename)

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)  # saving file at path specified by 'image_path'

            # detecting objects
            obj_ObjectDetector = ObjectDetector()
            detected_objects = obj_ObjectDetector.detect(image_path)

            # storing image to database
            obj_StoreImage = StoreImage()
            obj_StoreImage.store(image_path, detected_objects)
        else:
            flash('Allowed file types are : png, jpg, jpeg', 'error')  # displaying error message if file not allowed
            return redirect(request.url)
    flash('Uploaded!!!', 'info')  # displaying success message that all files are uploaded

    return render_template('upload.html', filenames=file_names)


# function for searching image
@flask_main_app.route('/search', methods=["POST", "GET"])
def search_image():
    file = request.files.get('input_image')
    image_names = []  # it will contain all image names returned from database
    if file:
        if allowed_file(file.filename):  # checking for allowed file
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)  # saving image to upload folder

            # detecting objects
            obj_ObjectDetector = ObjectDetector()
            detected_objects = obj_ObjectDetector.detect(image_path)

            # retrieving images
            obj_RetrieveImages = RetrieveImages()
            images_with_object = obj_RetrieveImages.retrieve(detected_objects)  # returned image paths from database

            # converting image paths to image names
            for i in images_with_object:
                image_names.append(i.split('/')[-1])
        else:
            flash('Allowed file types are : png, jpg, jpeg', 'error')  # displaying error message if file not allowed
            return redirect(request.url)
    return render_template('search.html', image_names=image_names)


# function to load images one by one using filename from upload folder
@flask_main_app.route('/search/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

