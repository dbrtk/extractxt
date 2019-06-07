
import os
import shlex
import subprocess

from .config.appconf import (DEFAULT_DPI, LANGUAGE, PDFTOTEXT_FILE_PREFIX,
                             PDFTOTEXT_SCRIPT, TMP_PATH)


def extract_from_pdf(pdf_path: str = None, unique_id: str = None):

    tmp_path = os.path.join(TMP_PATH, unique_id)
    os.mkdir(tmp_path)

    results = subprocess.run(
        shlex.split("sh {} -f {} -t {} -o {} --dpi {} --language {} --prefix {}".format(
            PDFTOTEXT_SCRIPT,
            pdf_path,
            tmp_path,
            unique_id,
            DEFAULT_DPI,
            LANGUAGE,
            PDFTOTEXT_FILE_PREFIX
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
