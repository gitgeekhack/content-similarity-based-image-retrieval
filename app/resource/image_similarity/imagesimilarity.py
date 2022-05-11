import os
from flask import Blueprint
from flask import flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from app.common.utils import allowed_file
from app.constant import UPLOAD_FOLDER, MAXIMUM_UPLOAD
from app.service.search_and_index_images import ImageIndexer, ImageSearcher

imgsimilarity_app = Blueprint('imgsimilarity', __name__)  # creating Blueprint for flask app

file = None

# rendering index.html on homepage of app
@imgsimilarity_app.route('/')
def homepage():
    return render_template('index.html')


# rendering indexing.html for uploading images
@imgsimilarity_app.route('/index')
def upload_form():
    return render_template('indexing.html')


# creating required objects
obj_imageindexer = ImageIndexer()
obj_imagesearcher = ImageSearcher()


# uploading and indexing image
@imgsimilarity_app.route('/index', methods=['POST'])
def index_images():
    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')

    if len(files) > MAXIMUM_UPLOAD:
        flash(f'Maximum {MAXIMUM_UPLOAD} files allowed at a time', 'warning')  # only 100 files allowed at a time
        return redirect(request.url)

    allowed_files = []  # allowed file list
    not_allowed_files = []  # not allowed file list

    for file in files:
        if allowed_file(file.filename):
            allowed_files.append(file)
        else:
            not_allowed_files.append(secure_filename(file.filename))

    file_with_paths = []
    for file in allowed_files:
        filename = secure_filename(file.filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)  # saving file at path specified by 'image_path'
        file_with_paths.append(image_path)

    image_indexed_count = obj_imageindexer.indeximages(file_with_paths)  # indexing images and storing to database

    # Displaying various flash messages

    # uploaded files contains some not allowed file
    if not_allowed_files:
        flash('Allowed file types are : png, jpg, jpeg', 'error')

    # displaying all files which are uploaded
    if allowed_files:
        flash(f'Total images indexed: {image_indexed_count}, Already present in index: {len(allowed_files) - image_indexed_count}', 'info')

    return render_template('indexing.html')


# function for searching image
@imgsimilarity_app.route('/search', methods=["POST", "GET"])
def search_image():
    global file
    file = request.files.get('input_image')
    image_names = []  # it will contain all image names returned from database
    filename = None
    if file:
        if allowed_file(file.filename):  # checking for allowed file
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)  # saving image to upload folder

            # detecting objects
            file_with_paths = [image_path]
            similar_images = obj_imagesearcher.searchimages(file_with_paths, range_search=False)  # searching similar images

            if not similar_images:
                flash('No similar images found',
                      'warning')  # display warning if no similar images found
                render_template('searching.html', image_names=image_names, search_image=filename)

            if similar_images == 'No index':
                flash('Faiss index not available, first create it by indexing images',
                      'warning')  # display warning if faiss index not available
                return redirect(request.url)

            # converting image paths to image names
            for i in similar_images:
                image_names.append(i.split('/')[-1])
        else:
            flash('Allowed file types are : png, jpg, jpeg', 'error')  # displaying error message if file not allowed
            return redirect(request.url)
    return render_template('searching.html', image_names=image_names, search_image=filename)


# function to load images one by one using filename from upload folder
@imgsimilarity_app.route('/search/<filename>')
def send_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# function for searching similar images based on distance threshold
@imgsimilarity_app.route('/load_more')
def search_multiple():
    global file

    image_names = []  # it will contain all image names returned from database
    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    file_with_paths = [image_path]
    similar_images = obj_imagesearcher.searchimages(file_with_paths, range_search=True)  # searching similar images

    # converting image paths to image names
    for i in similar_images:
        image_names.append(i.split('/')[-1])

    return render_template("range_search.html", image_names=image_names)



