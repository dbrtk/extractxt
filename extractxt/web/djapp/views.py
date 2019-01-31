import json
import tempfile
import uuid

from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

from ...config import (
    ALLOWED_CONTENT_TYPES, CORPUS_ENDPOINT, CORPUS_DATA_ENDPOINT,
    CREATE_CORPUS_ENDPOINT, DEFAULT_ENCODING, EXPECTED_FILES_ENDPOINT)
from ...task import process_files


@csrf_exempt
def upload_files(request):

    req_obj = request.POST.dict()
    the_name = req_obj.get('name')
    corpusid = req_obj.get('corpusid', None)

    file_objects = []
    for _file in request.FILES.getlist('files'):
        if _file.content_type not in ALLOWED_CONTENT_TYPES:
            continue
        file_data = {
            'file_name': _file.name,
            'unique_id': uuid.uuid4().hex,
            'content_type': _file.content_type,
            'charset': _file.charset or DEFAULT_ENCODING
        }
        with tempfile.NamedTemporaryFile(delete=False) as outf:
            file_data['tmp_file'] = outf.name
            for line in _file.readlines():
                outf.write(line)
        file_objects.append(file_data)
    if corpusid:
        requests.post(EXPECTED_FILES_ENDPOINT, data={
            'corpusid': corpusid, 'file_objects': json.dumps(file_objects)})
        resp = requests.get(
            CORPUS_DATA_ENDPOINT, params={'corpusid': corpusid})
        resp = resp.json()
        corpus_files_path = resp.get('corpus_files_path')
    else:
        resp = requests.post(
            CREATE_CORPUS_ENDPOINT,
            json={'name': the_name, 'file_objects': file_objects})
        resp = resp.json()
        corpusid = resp.get('corpusid')
        corpus_files_path = resp.get('corpus_files_path')

    process_files.delay(corpusid=corpusid,
                        corpus_files_path=corpus_files_path,
                        file_objects=file_objects)
    return HttpResponseRedirect('{}{}/'.format(CORPUS_ENDPOINT, corpusid))


def home(request):

    return JsonResponse({
        'msg': "Hello world!"
    })
