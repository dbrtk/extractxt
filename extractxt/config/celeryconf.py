
from .appconf import BROKER_HOST_NAME, REDIS_PASS


_url = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:6379/0'

BROKER_URL = _url
CELERY_RESULT_BACKEND = _url


CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_IMPORTS = ('extractxt.tasks', )

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ROUTES = {

    'extractxt.tasks.*': {'queue': 'extractxt'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},
}

RMXBOT_TASKS = {

    'expected_files': 'rmxbot.tasks.container.expected_files',

    'create': 'rmxbot.tasks.container.create_from_upload',

    'file_extract_callback': 'rmxbot.tasks.container.file_extract_callback',

    'create_data_from_file': 'rmxbot.tasks.data.create',

}

