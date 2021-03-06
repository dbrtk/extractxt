# import json
# import os
# import shlex
# import stat
# import subprocess
# import tempfile
# import uuid
#
# from django.http import HttpResponseRedirect, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests
#
# from ...config import (
#     ALLOWED_CONTENT_TYPES, CORPUS_ENDPOINT, CORPUS_DATA_ENDPOINT,
#     CORPUS_STATUS, CREATE_CORPUS_ENDPOINT, DEFAULT_ENCODING,
#     EXPECTED_FILES_ENDPOINT, TMP_PATH)
# from ...tasks import process_files
#
#
# @csrf_exempt
# def upload_files(request):
#
#     req_obj = request.POST.dict()
#     the_name = req_obj.get('name')
#     corpusid = req_obj.get('corpusid', None)
#
#     file_objects = []
#     not_allowed = []
#     for _file in request.FILES.getlist('files'):
#
#         file_data = {
#             'file_name': _file.name,
#             'unique_id': uuid.uuid4().hex,
#             'charset': _file.charset or DEFAULT_ENCODING
#         }
#         outf_path = '{}/{}'.format(TMP_PATH, uuid.uuid4().hex)
#         with open(outf_path, 'b+a') as outf:
#             for line in _file.readlines():
#                 outf.write(line)
#         file_data['tmp_file'] = outf_path
#         os.chmod(outf_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
#
#         ctype = get_mimetype(file_data['tmp_file'])
#
#         file_data['content_type'] = ctype
#         if ctype in ALLOWED_CONTENT_TYPES:
#             file_objects.append(file_data)
#         else:
#             not_allowed.append(file_data)
#             os.remove(file_data['tmp_file'])
#
#     if not file_objects:
#         return JsonResponse({
#             'success': False,
#             'error': True,
#             'files': not_allowed,
#             'msg': 'Only the following content-types are supported:%r'
#                      % ALLOWED_CONTENT_TYPES
#         })
#     if corpusid:
#         requests.post(EXPECTED_FILES_ENDPOINT, data={
#             'corpusid': corpusid, 'file_objects': json.dumps(file_objects)})
#         resp = requests.get(
#             CORPUS_DATA_ENDPOINT, params={'corpusid': corpusid})
#         resp = resp.json()
#         corpus_files_path = resp.get('corpus_files_path')
#         status = CORPUS_STATUS['upload']
#     else:
#         resp = requests.post(
#             CREATE_CORPUS_ENDPOINT,
#             json={'name': the_name, 'file_objects': file_objects})
#         resp = resp.json()
#         corpusid = resp.get('corpusid')
#         corpus_files_path = resp.get('corpus_files_path')
#         status = CORPUS_STATUS['new']
#
#     process_files.delay(corpusid=corpusid,
#                         corpus_files_path=corpus_files_path,
#                         file_objects=file_objects)
#     return HttpResponseRedirect(
#         '{}{}/?status={}'.format(CORPUS_ENDPOINT, corpusid, status))
#
#
# def home(request):
#
#     return JsonResponse({
#         'msg': "Hello world!"
#     })
#
#
# def get_mimetype(path: str = None) -> str:
#     """Using the file command to retrieve the mime type of a file."""
#     result = subprocess.run(
#         shlex.split("file -b --mime-type {}".format(path)),
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         encoding="utf-8",
#         check=True,
#     )
#     return result.stdout.strip()
