import os
import shlex
import subprocess

from .config.appconf import PROCESS_TXT_SCRIPT


def process_text(file_path: str = None, unique_id: str = None,
                 corpus_files_path: str = None):

    results = subprocess.run(
        shlex.split("sh {} -f {} -t {} -o {}".format(
            PROCESS_TXT_SCRIPT,
            file_path,
            corpus_files_path,
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
        'file_path': os.path.join(corpus_files_path, unique_id),
    }
