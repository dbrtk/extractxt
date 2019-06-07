
import shlex
import subprocess

from chardet import UniversalDetector


def get_encoding(path: str = None):

    result = subprocess.run(
        shlex.split(" file -b --mime-encoding %s" % path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def run_chardet(detector: UniversalDetector= None, path: str = None) -> dict:

    if not detector:
        detector = UniversalDetector()
    else:
        detector.reset()
    with open(path, 'rb') as _file:
        for _line in _file.readlines():
            detector.feed(_line)
            if detector.done:
                break
    return detector.result

