
import os
import tempfile
import uuid

from django.http import HttpResponseRedirect, JsonResponse
import requests

from ...config import (ALLOWED_CONTENT_TYPES,
                       CORPUS_ENDPOINT, CREATE_CORPUS_ENDPOINT)
from ...task import process_files

# Create your views here.


def upload_files_corpus(request):

    pass


def upload_files(request):

    the_name = request.POST.get('name')
    encoding = request.POST.get('encoding', 'utf-8')
    corpusid = request.POST.get('id', None)

    file_objects = []
    for _file in request.FILES.getlist('files'):
        if _file.content_type not in ALLOWED_CONTENT_TYPES:
            continue
        file_data = {
            'file_name': _file.name,
            'unique_id': uuid.uuid4().hex,
            'content_type': _file.content_type,
            'charset': _file.charset
        }
        with tempfile.NamedTemporaryFile(delete=False) as outf:
            file_data['tmp_file'] = outf.name
            for line in _file.readlines():
                outf.write(line)
        file_objects.append(file_data)
    if corpusid:
        resp = {}
        corpusid = ''
        corpus_files_path = ''
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
