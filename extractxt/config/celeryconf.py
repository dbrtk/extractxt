
from .appconf import RPC_HOST, RPC_PASS, RPC_PORT, RPC_USER, RPC_VHOST

# redis config imports
from .appconf import BROKER_HOST_NAME, REDIS_DB_NUMBER, REDIS_PASS, REDIS_PORT


# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
_url = f'amqp://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}/{RPC_VHOST}'

broker_url = _url

# result_backend = 'rpc://'

# redis result backend
result_backend = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:{REDIS_PORT}/{REDIS_DB_NUMBER}'

result_persistent = True

result_expires = 30
timezone = 'UTC'

imports = ('extractxt.tasks', )

accept_content = ['json', 'msgpack', 'yaml']
task_serializer = 'json'
result_serializer = 'json'

task_routes = {

    'extractxt.tasks.*': {'queue': 'extractxt'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},
}

RMXBOT_TASKS = {

    'expected_files': 'rmxbot.tasks.container.expected_files',

    'create': 'rmxbot.tasks.container.create_from_upload',

    'file_extract_callback': 'rmxbot.tasks.container.file_extract_callback',

    'create_data_from_file': 'rmxbot.tasks.data.create',

}

