import os

from .app import celery
from .config.appconf import CONTENT_TYPES, DEFAULT_ENCODING
from .config.celeryconf import RMXBOT_TASKS
from .fromtxt import process_text
from .utils import get_encoding


@celery.task
def process_files(corpusid: str = None, corpus_files_path: str = None,
                  file_objects: list = None):
    for item in file_objects:
        item.update({
            'corpusid': corpusid,
            'corpus_files_path': corpus_files_path
        })
        extract_from_file.delay(**item)


@celery.task
def extract_from_file(corpusid: str = None,
                      corpus_files_path: str = None,
                      unique_id: str = None,
                      path: str = None,
                      content_type: str = None,
                      file_name: str = None,
                      **_):
    kwds = {
        'file_path': path,
        'unique_id': unique_id,
        'corpus_files_path': corpus_files_path,
    }
    if content_type == CONTENT_TYPES.get('txt'):
        resp = process_text(**kwds)
    else:
        raise TypeError(content_type)
    success = True if resp.get('returncode') == 0 else False

    if success:
        celery.send_task(RMXBOT_TASKS['create_data_from_file'], kwargs={
            'corpusid': corpusid,
            'fileid': unique_id,
            'path': resp.get('file_path'),
            'file_name': file_name,
            'encoding': get_encoding(
                path=os.path.join(corpus_files_path, unique_id)
            ) or DEFAULT_ENCODING,
            'success': success,
        }, link=celery.signature(RMXBOT_TASKS['file_extract_callback']))
    else:
        celery.send_task(RMXBOT_TASKS['file_extract_callback'], kwargs={
            'success': False,
            'corpusid': corpusid,
            'file_id': unique_id,
        })
    if os.path.exists(path):
        os.remove(path)


@celery.task
def extract_from_txt(file_path: str = None,
                     unique_id: str = None,
                     corpus_files_path: str = None):

    resp = process_text(file_path=file_path, unique_id=unique_id,
                        corpus_files_path=corpus_files_path)
    return True if resp.get('returncode') == 0 else False
