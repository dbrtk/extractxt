import os
import uuid

from flask import Blueprint, flash, jsonify, request, redirect

from .app import celery
from .config.appconf import (ALLOWED_CONTENT_TYPES, CORPUS_ENDPOINT,
                             CORPUS_STATUS, DEFAULT_ENCODING, UPLOAD_FOLDER)
from .config.celeryconf import RMXBOT_TASKS
from .tasks import process_files
from .utils import get_mimetype


main_app = Blueprint('rmxupload_app', __name__, root_path='/')


@main_app.route('/upload-files', methods=['POST'], strict_slashes=False)
def upload_files():

    the_name = request.form.get('name')
    corpusid = request.form.get('corpusid', None)

    file_objects = []
    not_allowed = []
    if 'file' not in request.files:

        flash('No file part')
        return redirect(request.referrer)

    for _file in request.files.getlist('file'):

        uid = uuid.uuid4().hex
        file_data = {
            'file_name': _file.filename,
            'unique_id': uid,
            'charset': DEFAULT_ENCODING
        }

        path = os.path.join(UPLOAD_FOLDER, uid)
        _file.save(path)
        file_data['path'] = path
        ctype = get_mimetype(path)

        file_data['content_type'] = ctype
        if ctype in ALLOWED_CONTENT_TYPES:
            file_objects.append(file_data)
        else:
            not_allowed.append(file_data)
            os.remove(path)

    if not file_objects:
        return jsonify({
            'success': False,
            'error': True,
            'files': not_allowed,
            'msg': 'Only the following content-types are supported:%r'
                     % ALLOWED_CONTENT_TYPES
        })
    if corpusid:

        resp = celery.send_task(
            RMXBOT_TASKS['expected_files'],
            kwargs={'corpusid': corpusid, 'file_objects': file_objects}
        ).get()
        corpus_files_path = resp.get('corpus_files_path')
        status = CORPUS_STATUS['upload']
    else:

        resp = celery.send_task(
            RMXBOT_TASKS['create'],
            kwargs={'name': the_name, 'file_objects': file_objects}).get()

        corpusid = resp.get('corpusid')
        corpus_files_path = resp.get('corpus_files_path')
        status = CORPUS_STATUS['new']

    process_files.delay(corpusid=corpusid,
                        corpus_files_path=corpus_files_path,
                        file_objects=file_objects)
    return redirect(
        '{}{}/?status={}'.format(CORPUS_ENDPOINT, corpusid, status))
