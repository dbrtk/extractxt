import json
import os
import tempfile
import uuid

from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import filetype
import requests

from ...config import (
    ALLOWED_CONTENT_TYPES, CORPUS_ENDPOINT, CORPUS_DATA_ENDPOINT,
    CORPUS_STATUS, CREATE_CORPUS_ENDPOINT, DEFAULT_ENCODING,
    EXPECTED_FILES_ENDPOINT)
from ...task import process_files


@csrf_exempt
def upload_files(request):

    req_obj = request.POST.dict()
    the_name = req_obj.get('name')
    corpusid = req_obj.get('corpusid', None)

    file_objects = []
    not_allowed = []
    for _file in request.FILES.getlist('files'):

        file_data = {
            'file_name': _file.name,
            'unique_id': uuid.uuid4().hex,
            # 'content_type': _file.content_type,
            'charset': _file.charset or DEFAULT_ENCODING
        }

        with tempfile.NamedTemporaryFile(delete=False) as outf:
            file_data['tmp_file'] = outf.name
            for line in _file.readlines():
                outf.write(line)

        ctype = filetype.guess(file_data['tmp_file']).mime
        file_data['content_type'] = ctype

        if ctype not in ALLOWED_CONTENT_TYPES:
            not_allowed.append(file_data)
            os.remove(file_data['tmp_file'])
            continue

        file_objects.append(file_data)

    import remote_pdb
    remote_pdb.set_trace(host='0.0.0.0', port=4444)

    if not file_objects:
        return JsonResponse({
            'success': False,
            'error': True,
            'files': not_allowed,
            'msg': 'Only the following content-types are supported:%r'
                     % ALLOWED_CONTENT_TYPES
        })
    if corpusid:
        requests.post(EXPECTED_FILES_ENDPOINT, data={
            'corpusid': corpusid, 'file_objects': json.dumps(file_objects)})
        resp = requests.get(
            CORPUS_DATA_ENDPOINT, params={'corpusid': corpusid})
        resp = resp.json()
        corpus_files_path = resp.get('corpus_files_path')
        status = CORPUS_STATUS['upload']
    else:
        resp = requests.post(
            CREATE_CORPUS_ENDPOINT,
            json={'name': the_name, 'file_objects': file_objects})
        resp = resp.json()
        corpusid = resp.get('corpusid')
        corpus_files_path = resp.get('corpus_files_path')
        status = CORPUS_STATUS['new']

    process_files.delay(corpusid=corpusid,
                        corpus_files_path=corpus_files_path,
                        file_objects=file_objects)
    return HttpResponseRedirect(
        '{}{}/?status={}'.format(CORPUS_ENDPOINT, corpusid, status))


def home(request):

    return JsonResponse({
        'msg': "Hello world!"
    })
