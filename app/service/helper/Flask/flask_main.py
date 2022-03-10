import os
from app.service.helper.Main import detect_objects, store_objects
from app.service.helper.Database.img_retrieve import multiple_key_retrieve
from app.manage import create_flask_app

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT[:-21]

UPLOAD_FOLDER = APP_ROOT+'/resource/Uploaded_images'

app = create_flask_app()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            detected_objects = detect_objects(image_path)
            store_objects(image_path, detected_objects)
        else:
            flash('Allowed file types are : png, jpg, jpeg', 'error')
            return redirect(request.url)
    flash('Done!!!', 'info')
    # print(file_names)
    return render_template('upload.html', filenames=file_names)


@app.route('/search', methods=["POST", "GET"])
def search_image():
    file = request.files.get('input_image')
    image_names = []
    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            detected_objects = detect_objects(image_path)
            images_with_keys = multiple_key_retrieve(detected_objects)
            for i in images_with_keys:
                image_names.append(i.split('/')[-1])
        else:
            flash('Allowed file types are : png, jpg, jpeg', 'error')
            return redirect(request.url)
    return render_template('search.html', image_names=image_names)


@app.route('/search/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

