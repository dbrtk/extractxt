
BROKER_URL = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

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

    'expected_files': 'rmxbot.tasks.corpus.expected_files',

    'create': 'rmxbot.tasks.corpus.create_from_upload',

    'file_extract_callback': 'rmxbot.tasks.corpus.file_extract_callback',

    'create_data_from_file': 'rmxbot.tasks.data.create',

}

