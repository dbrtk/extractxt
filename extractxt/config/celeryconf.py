from .appconf import BROKER_HOST_NAME

BROKER_URL = 'redis://{}:6379/0'.format(BROKER_HOST_NAME)
CELERY_RESULT_BACKEND = 'redis://{}:6379/0'.format(BROKER_HOST_NAME)

# BROKER_URL = f"amqp://rmxuser:rmxpass@{BROKER_HOST_NAME}:5672/rmxvhost"
# CELERY_RESULT_BACKEND = 'rpc://'


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

