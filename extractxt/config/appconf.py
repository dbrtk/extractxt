
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'bin')

PROCESS_TXT_SCRIPT = os.environ.get('PROCESSTXT_SCRIPT')

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

# RabbitMQ configuration
# RabbitMQ rpc queue name
# These values are defined on the level of docker-compose.
RPC_QUEUE_NAME = os.environ.get('RPC_QUEUE_NAME', 'extractxt')

# login credentials for RabbitMQ.
RPC_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RPC_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RPC_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')

# the host to which the rpc broker (rabbitmq) is deployed
RPC_HOST = os.environ.get('RABBITMQ_HOST')
RPC_PORT = os.environ.get('RABBITMQ_PORT', 5672)


# REDIS CONFIG
# celery, redis (auth access) configuration
BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER')
REDIS_PORT = os.environ.get('REDIS_PORT')

