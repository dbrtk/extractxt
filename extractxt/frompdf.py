
import os
import shlex
import subprocess

from .config.appconf import (DEFAULT_DPI, LANGUAGE, PDFTOTEXT_FILE_PREFIX,
                             PDFTOTEXT_SCRIPT, TMP_FOLDER)


def extract_from_pdf(file_path: str = None, unique_id: str = None,
                     corpus_files_path: str = None):

    tmp_path = os.path.join(TMP_FOLDER, unique_id)
    os.mkdir(tmp_path)

    results = subprocess.run(
        shlex.split("sh {} -f {} -t {} -p {} -o {} --dpi {} --language {} --prefix {}".format(
            PDFTOTEXT_SCRIPT,
            file_path,
            corpus_files_path,
            tmp_path,
            unique_id,
            DEFAULT_DPI,
            LANGUAGE,
            PDFTOTEXT_FILE_PREFIX
        )),
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    # if results.stderr:
    #     raise RuntimeError(results.stderr)
    return {
        'stdout': results.stdout,
        'returncode': results.returncode,
        'file_path': os.path.join(corpus_files_path, unique_id),
    }
