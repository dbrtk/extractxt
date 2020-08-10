
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'bin')

PROCESS_TXT_SCRIPT = os.environ.get('PROCESSTXT_SCRIPT')

BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')

DEFAULT_DPI = 300

TMP_FOLDER = os.environ.get('TMP_FOLDER')

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

LANGUAGE = 'eng'

PDFTOTEXT_FILE_PREFIX = 'file'


# todo(): remove all endpoints
# rmxbot
RMXBOT_ENDPOINT = os.environ.get('RMXBOT_ENDPOINT')

CORPUS_ENDPOINT = '{}/container/'.format(RMXBOT_ENDPOINT)

CORPUS_STATUS = {
    'new': 'newly-created',
    'upload': 'file-upload',
}


ALLOWED_CONTENT_TYPES = [

    'text/plain',
]

DEFAULT_ENCODING = 'utf8'

CONTENT_TYPES = {

    'txt': 'text/plain',
}

# celery, redis (auth access) configuration
REDIS_PASS = os.environ.get('REDIS_PASS')
