# importing required libraries
import os
from flask import Blueprint
from flask import flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from app.common.utils import allowed_file
from app.constant import UPLOAD_FOLDER
import time

# importing helper functions
from app.service.image_store_and_retrieve import ObjectDetector, StoreImage, RetrieveImages

flask_main_app = Blueprint('main_app', __name__)  # creating Blueprint for flask app


# rendering index.html on homepage of app
@flask_main_app.route('/')
def homepage():
    return render_template('index.html')


# rendering upload.html for uploading images
@flask_main_app.route('/upload')
def upload_form():
    return render_template('upload.html')


# creating required objects
obj_ObjectDetector = ObjectDetector()
obj_StoreImage = StoreImage()
obj_RetrieveImages = RetrieveImages()


# uploading and saving image
@flask_main_app.route('/upload', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')

    if len(files) > 5:
        flash('Maximum 5 files allowed at a time', 'warning')  # only 5 files allowed at a time
        return redirect(request.url)

    allowed_files = []  # allowed file list
    not_allowed_files = []  # not allowed file list
    images_with_no_objects = []  # images which doesn't contain objects

    for file in files:
        if allowed_file(file.filename):
            allowed_files.append(file)
        else:
            not_allowed_files.append(secure_filename(file.filename))

    for file in allowed_files:
        filename = secure_filename(file.filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)  # saving file at path specified by 'image_path'

        # detecting objects
        # a=time.time()  # for measuring execution time
        detected_objects = obj_ObjectDetector.detect(image_path)
        # print("Time for detecting objects from image",time.time() - a)  # displaying time taken

        # storing image to database
        if detected_objects:
            # b=time.time()  # for measuring execution time
            obj_StoreImage.store(image_path, detected_objects)
            # print("Time for storing objects to db",time.time() - b)  # displaying time taken
        else:
            images_with_no_objects.append(filename)

    # Displaying various flash messages

    # uploaded files contains some not allowed file
    if not_allowed_files:
        flash('Allowed file types are : png, jpg, jpeg', 'error')
        flash("This files are not allowed: "+str(not_allowed_files), "warning")

    # some uploaded images doesn't contain any objects
    if images_with_no_objects:
        flash("No objects detected in this images: "+str(images_with_no_objects), "warning")

    # displaying all files which are uploaded
    flash('Uploaded images: '+str([secure_filename(file.filename) for file in allowed_files if secure_filename(file.filename) not in images_with_no_objects]), 'info')

    return render_template('upload.html')


# function for searching image
@flask_main_app.route('/search', methods=["POST", "GET"])
def search_image():
    file = request.files.get('input_image')
    image_names = []  # it will contain all image names returned from database
    if file:
        if allowed_file(file.filename):  # checking for allowed file
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)  # saving image to upload folder

            # detecting objects
            # a=time.time()  # for time measuring
            detected_objects = obj_ObjectDetector.detect(image_path)
            # print("Time for detecting objects from image",time.time() - a)  # displaying time taken

            if not detected_objects:
                flash('No objects in given image, please try with another image',
                      'warning')  # displaying warning when no objects in input image
                return redirect(request.url)

            # retrieving images
            # b=time.time()  # for time measuring
            images_with_object = obj_RetrieveImages.retrieve(detected_objects)  # returned image paths from database
            if not images_with_object:
                flash('No similar images found, please try with another image',
                      'warning')  # displaying warning when no similar images found
                return redirect(request.url)
            # print("Time for retrieving images from db",time.time() - b)  # displaying time taken

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
    return send_from_directory(UPLOAD_FOLDER, filename)

