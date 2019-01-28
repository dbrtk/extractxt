
import os
import pathlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'bin')

PDFTOTEXT_SCRIPT = os.path.join(BIN_PATH, 'pdftotext.sh')

DEFAULT_DPI = 300

TMP_PATH = os.path.join(str(pathlib.Path.home()), 'Data', 'tmp')

LANGUAGE = 'eng'

PDFTOTEXT_FILE_PREFIX = 'file'

# rmxbot
RMXBOT_ENDPOINT = 'http://localhost:8000'

# celery broker and backend on rmxweb
RMXBOT_CELERY_BROKER = 'redis://localhost:6379/0'
RMXBOT_CELERY_BACKEND = 'redis://localhost:6379/0'

CREATE_CORPUS_ENDPOINT = '{}/corpus/create-from-upload/'.format(
    RMXBOT_ENDPOINT)

CORPUS_ENDPOINT = '{}/corpus/'.format(RMXBOT_ENDPOINT)

CREATE_DATA_ENDPOINT = '{}/data/create-from-file/'.format(RMXBOT_ENDPOINT)


FILE_EXTRACTION_CALLBACK = "{}/corpus/file-extract-callback/".format(
    RMXBOT_ENDPOINT)


ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'text/plain',
]

