
import os
import uuid

from celery import Celery
from flask import Flask

from .config import celeryconf


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'data')

SCRIPT_FOLDER = os.path.join(BASE_DIR, 'bin')

UPLOAD_FOLDER = os.path.join(DATA_ROOT, 'upload')
TMP_FOLDER = os.path.join(DATA_ROOT, 'tmp')

os.environ['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.environ['TMP_FOLDER'] = TMP_FOLDER

os.environ['PDFTOTXT_SCRIPT'] = os.path.join(SCRIPT_FOLDER, 'pdftotext.sh')
os.environ['PROCESSTXT_SCRIPT'] = os.path.join(SCRIPT_FOLDER, 'processtxt.sh')
os.environ['TMP_DIR_PATH'] = TMP_FOLDER
os.environ['RMXBOT_ENDPOINT'] = 'localhost:8000'


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
