
import shlex
import subprocess


def get_encoding(path: str = None):

    result = subprocess.run(
        shlex.split(" file -b --mime-encoding %s" % path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()
