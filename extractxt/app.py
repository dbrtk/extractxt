
import os
import uuid

from celery import Celery
from flask import Flask

from .config import celeryconf


UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']


def create_app():
    """Building up the flask applicaiton."""
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.secret_key = uuid.uuid4().hex

    with app.app_context():

        from .routes import main_app

        app.register_blueprint(main_app)

    return app


celery = Celery('extractxt')
celery.config_from_object(celeryconf)
