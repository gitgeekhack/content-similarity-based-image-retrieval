# importing required libraries
from flask import jsonify, make_response
from app.manage import create_app

app, logger = create_app()  # creating flask app using function

# importing Blueprint flask apps
from app.resource.common import common_app
from app.resource.flask_main import flask_main_app

# registering Blueprint flask apps
app.register_blueprint(common_app)
app.register_blueprint(flask_main_app)


# function for error handling
@app.errorhandler(404)
def page_not_found(e):
    """Default 404 handler"""
    return make_response(jsonify(ErrorMessage="Not found"), 404)
