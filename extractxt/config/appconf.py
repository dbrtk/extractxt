
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'bin')

# PDFTOTEXT_SCRIPT = os.path.join(BIN_PATH, 'pdftotext.sh')
# PROCESS_TXT_SCRIPT = os.path.join(BIN_PATH, 'processtxt.sh')

PDFTOTEXT_SCRIPT = os.environ.get('PDFTOTXT_SCRIPT')

PROCESS_TXT_SCRIPT = os.environ.get('PROCESSTXT_SCRIPT')

DEFAULT_DPI = 300

TMP_FOLDER = os.environ.get('TMP_FOLDER')

LANGUAGE = 'eng'

PDFTOTEXT_FILE_PREFIX = 'file'


# todo(): remove all endpoints
# rmxbot
RMXBOT_ENDPOINT = os.environ.get('RMXBOT_ENDPOINT')

CORPUS_ENDPOINT = '{}/corpus/'.format(RMXBOT_ENDPOINT)

CORPUS_STATUS = {
    'new': 'newly-created',
    'upload': 'file-upload',
}

# todo(): delete all endpoints - replace with celery
# CREATE_DATA_ENDPOINT = '{}/data/create-from-file/'.format(RMXBOT_ENDPOINT)
#
# TEXT_EXTRACT_CALLBACK = "{}/corpus/file-extract-callback/".format(
#     RMXBOT_ENDPOINT)



ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'text/plain',
]


DEFAULT_ENCODING = 'utf8'

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

