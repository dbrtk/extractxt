import os

from .app import celery
from .config.celeryconf import RMXBOT_TASKS
from .frompdf import extract_from_pdf
from .fromtxt import process_text
from .utils import run_chardet


CONTENT_TYPES = {
    'pdf': 'application/pdf',
    'txt': 'text/plain',
}


@celery.task
def process_files(corpusid: str = None, corpus_files_path: str = None,
                  file_objects: list = None):

    print('process files')

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
                      charset: str = None
                      ):
    print('extract_from_file')
    kwds = {
        'file_path': path,
        'unique_id': unique_id,
        'corpus_files_path': corpus_files_path,
    }
    if content_type == CONTENT_TYPES.get('pdf'):
        resp = extract_from_pdf(**kwds)
    elif content_type == CONTENT_TYPES.get('txt'):
        resp = process_text(**kwds)
    else:
        raise TypeError(content_type)
    res = run_chardet(path=os.path.join(corpus_files_path, unique_id))

    print('chardet res')
    print(res)

    celery.send_task(RMXBOT_TASKS['create_data_from_file'], kwargs={
        'corpusid': corpusid,
        'fileid': unique_id,
        'path': path,
        'file_name': file_name,
        'encoding': '',
        'success': True if resp.get('returncode') == 0 else False,
    }, link=update_corpus.s())


@celery.task
def update_corpus(corpusid: str = None,
                  success: bool = False,
                  data_id = None,
                  file_id: str = None,
                  file_name: str = None,
                  ):

    celery.send_task(RMXBOT_TASKS['file_extract_callback'], kwargs={
        'success': True,
        'corpusid': corpusid,
        'data_id': data_id,
        'file_name': file_name,
        'file_id': file_id,
    } if success else {
        'success': False,
        'corpusid': corpusid,
        'file_id': file_id,
    })

