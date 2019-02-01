import os
import shlex
import subprocess

from .config import PROCESS_TXT_SCRIPT, TMP_PATH


def process_text(file_path: str = None, unique_id: str = None):

    tmp_path = os.path.join(TMP_PATH, unique_id)
    os.mkdir(tmp_path)

    results = subprocess.run(
        shlex.split("sh {} -f {} -t {} -o {}".format(
            PROCESS_TXT_SCRIPT,
            file_path,
            tmp_path,
            unique_id,
        )),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        # capture_output=True,
        check=True,
    )
    return {
        'stdout': results.stdout,
        'returncode': results.returncode,
        'tmp_path': tmp_path,
        'file_path': os.path.join(tmp_path, '{}.txt'.format(unique_id))
    }
