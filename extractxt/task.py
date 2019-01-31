
import os
import shutil

from celery import shared_task
import requests

from .config import (CREATE_DATA_ENDPOINT, TEXT_EXTRACT_CALLBACK)
from .frompdf import extract_from_pdf


CONTENT_TYPES = {
    'pdf': 'application/pdf',
    'txt': 'text/plain',
}


@shared_task(bind=True)
def process_files(self, corpusid: str = None, corpus_files_path: str = None,
                  file_objects: list = None):

    for item in file_objects:
        item.update({
            'corpusid': corpusid,
            'corpus_files_path': corpus_files_path
        })
        extract_from_file.apply_async(kwargs=item, link=extract_callback.s())


@shared_task(bind=True)
def extract_from_file(self,
                      corpusid: str = None,
                      corpus_files_path: str = None,
                      unique_id: str = None,
                      tmp_file: str = None,
                      content_type: str = None,
                      file_name: str = None,
                      charset: str = None,
                      **_):

    if content_type == CONTENT_TYPES.get('pdf'):
        resp = extract_from_pdf(tmp_file, unique_id)
    elif content_type == CONTENT_TYPES.get('txt'):
        resp = {}
    else:
        raise TypeError(content_type)

    return {
        'unique_id': unique_id,
        'corpusid': corpusid,
        'corpus_files_path': corpus_files_path,
        'filename': file_name,
        'content_type': content_type,
        'charset': charset,

        'tmp_path': resp.get('tmp_path'),
        'file_path': resp.get('file_path'),
        'success': True if resp.get('returncode') == 0 else False,
        'stdout': resp.get('stdout'),
    }


@shared_task(bind=True)
def extract_callback(self, kwds: dict = None):

    resp = requests.post(
        CREATE_DATA_ENDPOINT,
        data={
            'corpusid': kwds.get('corpusid'),
            'corpus_files_path': kwds.get('corpus_files_path'),
            'unique_id': kwds.get('unique_id'),
            'success': kwds.get('success'),
            'file_name': kwds.get('filename'),
            'content_type': kwds.get('content_type'),
            'stdout': kwds.get('stdout'),
            'charset': kwds.get('charset'),
        },
        files={'file': open(kwds.get('file_path'), 'rb')}
    )
    resp = resp.json()

    shutil.rmtree(kwds.get('tmp_path'))
    if os.path.isdir(kwds.get('tmp_path')):
        raise RuntimeError(kwds.get('tmp_path'))

    requests.post(
        TEXT_EXTRACT_CALLBACK,
        data={
            'corpusid': kwds.get('corpusid'),
            'unique_id': kwds.get('unique_id'),
            'data_id': resp.get('data_id'),
            'file_path': resp.get('file_path'),
            'file_name': resp.get('file_name'),
            'file_id': resp.get('file_id')
        }
    )
